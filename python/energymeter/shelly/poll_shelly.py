import requests, logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WritePrecision

logger = logging.getLogger("shelly")

class ShellyPoller():
    def __init__(self, props, shelly_url):
        self.client = InfluxDBClient(url=props['influx']['url'], token=props['influx']['token'], org=props['influx']['org'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS) 
        self.shelly_url = shelly_url

        self.req = requests.Session()
        retries = Retry(total=10, backoff_factor=0.3, status_forcelist=[ 400, 404, 500 ])
        self.req.mount('http://', HTTPAdapter(max_retries=retries))

    def poll(self):
        logger.info("Polling shelly at {0}".format(self.shelly_url))
        r = self.req.get(self.shelly_url)
        res = r.json()

        res_time = res['timestamp']
        res_counters = res['counters']
        watt_hours = list(map(lambda x: x/60, res_counters))

        minutes = []
        minutes.append(res_time - (res_time % 60))
        minutes.append(minutes[0] - 60)
        minutes.append(minutes[1] - 60)

        logger.info("Received {0} at {1}".format(res_counters, minutes))

        return minutes, watt_hours

    def run(self):
        minutes, watt_hours = self.poll()   

        for min, wh in zip(minutes, watt_hours):
            logger.info("Processing {0} Wh at {1} to DB".format(wh, min))
            p = Point("energy").tag("meter", "solar").field("wh", wh).time(min, write_precision=WritePrecision.S)
            self.write_api.write(bucket=self.props['influx']['bucket'], record=p)

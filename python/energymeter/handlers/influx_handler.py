import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WritePrecision

logger = logging.getLogger("influx")

class InfluxHandler():
    def __init__(self, props):
        self.props = props
        self.client = InfluxDBClient(url=props['influx']['url'], token=props['influx']['token'], org=props['influx']['org'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)  

    def process_main(self,timestamp):
        p = Point("energy").tag("meter", "main").field("tick", 1).time(timestamp, write_precision=WritePrecision.MS)
        self.write_api.write(bucket=self.props['influx']['bucket'], record=p)

    def process_solar(self,timestamp, wh):
        p = Point("energy").tag("meter", "solar").field("wh", wh).time(timestamp, write_precision=WritePrecision.S)
        self.write_api.write(bucket=self.props['influx']['bucket'], record=p)


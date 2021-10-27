import logging, time
from gpiozero import LineSensor
from signal import pause
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, WritePrecision

logger = logging.getLogger("ingest")

class Sensor():
    def __init__(self, props):
        self.impulses = {}
        self.client = InfluxDBClient(url=props['influx']['url'], token=props['influx']['token'], org=props['influx']['org'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS) 

    def line_detected(self):
        nowSeconds = int(time.time())
        lastMinuteSeconds = nowSeconds - (nowSeconds % 60)
        nextMinuteSeconds = lastMinuteSeconds + 60

        logger.info("Line detected at {0}".format(nowSeconds))
       
        if nextMinuteSeconds in self.impulses:
            self.impulses[nextMinuteSeconds] += 1
        else:
            self.impulses[nextMinuteSeconds] = 1

        for timestamp in self.impulses:
            if timestamp <= lastMinuteSeconds:                
                wh = self.impulses[timestamp] / 10000 * 1000
                logger.info("Writing {0}Wh into DB at {1}".format(wh, timestamp))
                p = Point("energy").tag("meter", "main").field("wh", wh).time(timestamp, write_precision=WritePrecision.S)
                self.write_api.write(bucket=self.props['influx']['bucket'], record=p)

    def run(self):
        sensor = LineSensor(18, sample_rate=1000, queue_len=1)
        sensor.when_line = self.line_detected
        pause()

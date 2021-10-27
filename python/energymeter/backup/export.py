import logging
from datetime import datetime
from influxdb_client import InfluxDBClient

logger = logging.getLogger("backup")

class Exporter():
    def __init__(self, props):
        self.client = InfluxDBClient(url=props['influx']['url'], token=props['influx']['token'], org=props['influx']['org'])
        self.query_api = self.client.query_api()
    
    def day(self):
        return datetime.now().strftime("%Y-%m-%d")

    def export(self):
        self._export_meter("solar")
        self._export_meter("main")

    def _export_meter(self, name):
        tables = self.query_api.query(f"""
            from(bucket: "energy")
            |> range(start: today(), stop: now())
            |> filter(fn: (r) => r["_field"] == "wh")
            |> filter(fn: (r) => r["meter"] == "{name}")
        """)

        for rec in tables[0].records:
            with open("{0}/{2}-{1}.csv".format(self.root_dir, self.day(), name), "a+") as myfile:
                myfile.write("{0},{1}\n".format(rec['_time'], rec['_value']))


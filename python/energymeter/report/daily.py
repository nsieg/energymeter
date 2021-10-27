import logging
from influxdb_client import InfluxDBClient

logger = logging.getLogger("report")

class Reporter():
    def __init__(self, props, tele):
        self.client = InfluxDBClient(url=props['influx']['url'], token=props['influx']['token'], org=props['influx']['org'])
        self.query_api = self.client.query_api()
        self.tele = tele

    def report(self):
        tables = self.query_api.query('''
            import "date"
            import "experimental"

            from(bucket: "energy")
            |> range(start: experimental.subDuration(d: 1d, from: today()), stop: today())
            |> filter(fn: (r) => r["_field"] == "wh")
            |> filter(fn: (r) => r["meter"] == "solar")  
            |> sum(column: "_value")
            |> map(fn: (r) => ({r with _value: r._value / 1000.0 }))
        ''')

        val = tables[0].records[0]["_value"]
        self.tele.send("Guten Morgen! Gestern hat die Solaranlage {:3.2f} kWh produziert!".format(val))

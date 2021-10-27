import requests, logging

logger = logging.getLogger("shelly")

class ShellyPoller():
    def __init__(self, shelly_url, influx, file):
        self.shelly_url = shelly_url
        self.handlers = [ influx, file ]
        self.influx = influx

    def poll(self):
        logger.info("Polling shelly at {0}".format(self.shelly_url))
        r = requests.get(self.shelly_url)
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
            for h in self.handlers:
                logger.info("Processing {0} Wh at {1} with {2}".format(wh, min, type(h).__name__))
                h.process_solar(min, wh)

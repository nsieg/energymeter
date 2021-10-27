import logging, time
from gpiozero import LineSensor
from signal import pause

logger = logging.getLogger("ingest")

class Ingest():
    def __init__(self, handlers):
        self.handlers = handlers
        self.impulses = {}

    def line_detected(self):
        nowSeconds = int(time.time())
        lastMinuteSeconds = nowSeconds - (nowSeconds % 60)
        nextMinuteSeconds = lastMinuteSeconds + 60

        logger.info("Line detected at {0}".format(nowSeconds))
       
        if nextMinuteSeconds in self.impulses:
            self.impulses[nextMinuteSeconds] += 1
        else:
            self.impulses[nextMinuteSeconds] = 1

        for key in self.impulses:
            if key <= lastMinuteSeconds:
                for h in self.handlers:
                    logger.info("Processing line with {0}".format(type(h).__name__))
                    wh = self.impulses[key] / 10000 * 1000
                    h.process_main(key, wh)       

    def run(self):
        sensor = LineSensor(18, sample_rate=1000, queue_len=10)
        sensor.when_line = self.line_detected
        pause()

import logging, time
from gpiozero import LineSensor
from signal import pause

logger = logging.getLogger("ingest")

class Ingest():
    def __init__(self, handlers):
        self.handlers = handlers

    def line_detected(self):
        timeMillis = int(time.time() * 1000)
        logger.info("Line detected at {0}".format(timeMillis))
        for h in self.handlers:
            logger.info("Processing line with {0}".format(type(h).__name__))
            h.process_main(timeMillis)

    def run(self):
        sensor = LineSensor(18, sample_rate=1000, queue_len=10)
        sensor.when_line = self.line_detected
        pause()

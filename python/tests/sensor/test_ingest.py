import threading, unittest
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from time import sleep
from energymeter.sensor.ingest import Ingest
import multiprocessing
from multiprocessing.managers import BaseManager

def simulate():
    pin = MockFactory().pin(18)
    while True:
        for i in range(0,15):
            pin.drive_low()
            sleep(0.001)
        pin.drive_high()
        sleep(0.01)   

def process(handler):
    Device.pin_factory = MockFactory()
    threading.Thread(target=simulate).start()
    Ingest([handler]).run()

class DummyHandler():
    def __init__(self):
        self.counter = 0

    def process_main(self,txt):
        print(txt)
        self.counter = self.counter + 1

    def get_count(self):
        return self.counter

class Test(unittest.TestCase):
    def test(self):
        # Given
        # Handler needs to be thread and process safe
        BaseManager.register('Handler', DummyHandler)
        manager = BaseManager()
        manager.start()
        handler = manager.Handler()
        # Run async activity in process as threads block due to signal.pause
        p_sim = multiprocessing.Process(target=process, args=(handler,))

        # When: ingest listens and receives line signals
        p_sim.start()
   
        # Then: handler is called 
        while handler.get_count() < 5:
            sleep(0.01)     

        p_sim.terminate()
       
if __name__ == "__main__": 
    unittest.main()
import unittest, time
from energymeter.handlers import influx_handler

class Test(unittest.TestCase):

    @unittest.skip("only works with influx running")
    def test(self):
        # Given
        props = dict(
            influx = dict(
                token = "bprkRJcSdwTsfamvIeCeUgxNSZTLBcdGDyqKHntyrEbeH9MkZdtIfTnamhwHHybTvUEE9qNkljt6A41XoGaMWQ==",
                url = "http://localhost:8086",
                org = "siegfried",
                bucket = "energymeter"
            )
        )
        handler = influx_handler.InfluxHandler(props)

        # When
        for i in range(0,5):
            handler.process(int(time.time() * 1000))
            time.sleep(1.001)

        # Then
        # Check manually in influx

if __name__ == "__main__": 
    unittest.main()
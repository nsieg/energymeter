import unittest
from unittest.mock import patch
from energymeter.shelly import poll_shelly

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({
        "power": 20,
        "overpower": 23.78,
        "is_valid": "true",
        "timestamp": 1625170013,
        "counters": [26,25,28],
        "total": 250
    }, 200)

class Test(unittest.TestCase):
    def setUp(self):
        self.props = dict(
            influx = dict(
                token = "",
                url = "http://localhost:8086",
                org = "demoorg",
                bucket = "energy"
            )
        )

    @unittest.skip("only works with influx running")
    def test_influx(self):
        # Given    
        poller = poll_shelly.ShellyPoller(self.props, "")

        # When
        poller.record_exists(1622970355)
        poller.record_exists(1522970355)

    @patch('poll_shelly.requests.get', side_effect=mocked_requests_get)
    def test_shelly_api(self, mock):
        # Given
        poller = poll_shelly.ShellyPoller(self.props, "")
        mock.return_value.ok = True

        # When
        mins, whs = poller.poll()

        # Then
        self.assertEqual(whs[1],25/60)


    @unittest.skip("only works with influx running")
    @patch('poll_shelly.requests.get', side_effect=mocked_requests_get)
    def test_shelly_api(self, mock):
        # Given
        poller = poll_shelly.ShellyPoller(self.props, "")
        mock.return_value.ok = True

        # When
        poller.run()

    @unittest.skip("only works with influx & shelly running")
    def test_shelly_api(self):
        # Given
        poller = poll_shelly.ShellyPoller(self.props, "http://192.168.168.151/meter/0")

        # When
        poller.run()

if __name__ == "__main__": 
    unittest.main()
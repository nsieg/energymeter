import unittest
from energymeter.report import daily

class Test(unittest.TestCase):
    def setUp(self):
        self.props = dict(
            influx = dict(
                token = "21h2KowbVs7EpnQKvnRTNPlRv3h9zIEpHLFTgiBHspCDCf3SWZPP6s7D_RykAYlwWJL4nirQRXByuSO_Y7gEYA==",
                url = "http://192.168.168.128:8086",
                org = "siegfried",
                bucket = "energy"
            )
        )
        self.tele = False

    def test_daily_live(self):
        reporter = daily.Reporter(self.props, self.tele)
        reporter.report()


if __name__ == "__main__": 
    unittest.main()
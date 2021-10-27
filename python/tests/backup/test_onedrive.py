import unittest
from energymeter.backup import onedrive

class Test(unittest.TestCase):
    @unittest.skip("only works with credentials")
    def test_connect(self):
        # Given
        props = dict(
            onedrive = dict(
                clientSecret = '',
                clientId = '',
                redirectUri = 'http://localhost:8080/.auth/login/aad/callback'
            )
        )
        drive = onedrive.Onedrive(props)

        # When
        drive.connect() 
        drive.upload("/home/nils/energymeter/python/src/ingest.py","ingest.py","energymeter/main")

if __name__ == "__main__": 
    unittest.main()

import unittest, os
from unittest.mock import patch
from tempfile import TemporaryDirectory
from energymeter.backup import backup

class Test(unittest.TestCase):

    @patch('energymeter.backup.onedrive.Onedrive')
    def test_backup(self, M_Onedrive):
        # Given
        m_onedrive = M_Onedrive()

        with TemporaryDirectory() as dir:
            back = backup.Backup(m_onedrive, dir)

            with open(os.path.join(dir, 'main-2021-05-05.csv'),"w") as f1:
                f1.write('Hello world!')
            with open(os.path.join(dir, 'solar-2021-04-05.csv'),"w") as f1:
                f1.write('Hello world!')

            print(f1.name)
         
            # When
            back.backup()

            # Then
            M_Onedrive.return_value.connect.assert_called_once()
            M_Onedrive.return_value.upload.assert_any_call(os.path.join(dir, 'main-2021-05-05.csv'), "main-2021-05-05.csv", "energymeter/main")
            M_Onedrive.return_value.upload.assert_any_call(os.path.join(dir, 'solar-2021-04-05.csv'), "solar-2021-04-05.csv", "energymeter/solar")
            with self.assertRaises(FileNotFoundError):
                open(os.path.join(dir, 'main-2021-05-05.csv'),"r")
                open(os.path.join(dir, 'solar-2021-04-05.csv'),"r")

if __name__ == "__main__": 
    unittest.main()
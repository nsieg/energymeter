import unittest, time, os
from datetime import datetime
from energymeter.handlers import file_handler

class Test(unittest.TestCase):

    def test_main(self):
        # Given
        handler = file_handler.FileHandler(".")

        # When
        for i in range(0,5):
            handler.process_main(int(time.time() * 1000))
            time.sleep(0.001)

        # Then
        filename = 'main-{0}.csv'.format(datetime.now().strftime("%Y-%m-%d"))
        with open(filename, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines),5)
        os.remove(filename)

    def test_solar(self):
        # Given
        handler = file_handler.FileHandler(".")
        filename = 'solar-{0}.csv'.format(datetime.now().strftime("%Y-%m-%d"))
        if os.path.exists(filename):
            os.remove(filename)

        # When
        for i in range(0,5):
            handler.process_solar(int(time.time() * 1000), 0.5)
            time.sleep(0.001)

        # Then
        with open(filename, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines),5)
        os.remove(filename)

    def test_solar_duplicates(self):
        # Given
        handler = file_handler.FileHandler(".")
        filename = 'solar-{0}.csv'.format(datetime.now().strftime("%Y-%m-%d"))
        if os.path.exists(filename):
            os.remove(filename)

        # When
        thedate = int(time.time() * 1000)
        for i in range(0,5):
            handler.process_solar(thedate, 0.5)
            time.sleep(0.001)
        handler.process_solar(thedate + 2, 0.5)
        handler.process_solar(thedate, 0.6)
        handler.process_solar(thedate, 0.5)

        # Then
        with open(filename, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines),3)
        os.remove(filename)

if __name__ == "__main__": 
    unittest.main()
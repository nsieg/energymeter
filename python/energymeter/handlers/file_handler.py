from datetime import datetime
import csv, logging

logger = logging.getLogger("file")

class FileHandler():
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def day(self):
        return datetime.now().strftime("%Y-%m-%d")

    def process_main(self,timestamp):
        with open("{0}/main-{1}.csv".format(self.root_dir, self.day()), "a") as myfile:
            myfile.write("{0}\n".format(timestamp))

    def process_solar(self,timestamp, wh):
        with open("{0}/solar-{1}.csv".format(self.root_dir, self.day()), "a+") as myfile:
            myfile.seek(0, 0)
            csv_file = csv.DictReader(myfile, fieldnames=["ts", "wh"])
            for row in csv_file:
                if int(dict(row)['ts']) == timestamp and float(dict(row)['wh']) == wh:
                    logger.info("Already found {0} at {1} in data file".format(timestamp, wh))
                    return
            myfile.write("{0},{1}\n".format(timestamp, wh))

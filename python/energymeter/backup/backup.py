import glob, datetime, logging
from datetime import date
from subprocess import run

logger = logging.getLogger("backup")

class Backup():
    def __init__(self, onedrive, root_dir):
        self.onedrive = onedrive
        self.root_dir = root_dir

    def __getBackupFiles(self):
        files = []
        for file in glob.iglob(self.root_dir + '**/*.csv', recursive=True):
            logger.info("Found file {0}".format(file))  
            file_name = file.split("/")[-1] 
            file_meter = file_name.split("-",1)[0]
            file_date_string = (file_name.split("-",1)[1]).split(".")[0]
            file_date = datetime.datetime.strptime(file_date_string, '%Y-%m-%d').date()
            if date.today() > file_date:
                logger.info("Added file {0} for backup".format(file_name))
                files.append(dict(file=file, name=file_name, path=file_meter))
        return files

    def backup(self):
        self.onedrive.connect()
        for f in self.__getBackupFiles():
            logger.info("Uploading file {0} to Onedrive".format(f['name']))
            self.onedrive.upload(f['file'], f['name'], "energymeter/{0}".format(f['path']))
            run(['rm', '-f', f['file']])

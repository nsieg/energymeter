import backup, onedrive, export
from energymeter.util import main_helper

def main_backup(props,tele):
    drive = onedrive.Onedrive(props)
    exporter = export.Exporter(props)
    exporter.export()
    backuper = backup.Backup(drive, props['backup']['dir'])
    backuper.backup()

main_helper.main(main_backup, "backup")

import ingest
from energymeter.handlers import influx_handler, file_handler
from energymeter.util import main_helper

def main_ingest(props,tele):
    file_h = file_handler.FileHandler(props['backup']['dir'])
    influx_h = influx_handler.InfluxHandler(props)
    handlers = [file_h, influx_h]

    ingester = ingest.Ingest(handlers)
    ingester.run()

main_helper.main(main_ingest, "ingest")

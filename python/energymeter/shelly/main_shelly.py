from energymeter.handlers import influx_handler, file_handler
from energymeter.util import main_helper
import poll_shelly

def main_shelly(props,tele):
    file_h = file_handler.FileHandler(props['backup']['dir'])
    influx_h = influx_handler.InfluxHandler(props)

    poller = poll_shelly.ShellyPoller(props['shelly']['url'], influx_h, file_h)
    poller.run()

main_helper.main(main_shelly, "shelly")

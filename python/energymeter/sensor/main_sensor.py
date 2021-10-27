import fetch_sensor
from energymeter.handlers import influx_handler, file_handler
from energymeter.util import main_helper

def main_sensor(props, tele):
    sensor = fetch_sensor.Sensor()
    sensor.run()

main_helper.main(main_sensor, "sensor")

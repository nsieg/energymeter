import logging, json, logging.config
from energymeter.telegram import telegram

with open("../../config/properties.json", "r") as f:
    props = json.load(f)

with open("../../config/log_config.json", "r") as f:
    logging.config.dictConfig(json.load(f))

tele = telegram.Sender(props['telegram']['bot_id'], props['telegram']['chat_id'])

def main(myfun, name):
    try:
        logger = logging.getLogger(name)
        logger.info("Starting main {0}".format(name))

        myfun(props,tele)
    except Exception as e:
        tele.send("Fehler in main {0}! Bitte Logs kontrollieren.".format(name))
        logger.exception("main %s crashed. Error: %s", name, e)

import requests, logging

logger = logging.getLogger("telegram")

class Sender():
    def __init__(self, bot_id, chat_id):
        self.bot_id = bot_id
        self.chat_id = chat_id

    def send(self, msg):
        params = {
            "chat_id" : self.chat_id, 
            "text" : msg
        }
        url = "https://api.telegram.org/bot{0}/sendMessage".format(self.bot_id)
        
        try:
            logger.info("Sending {0} to chat {1}".format(msg,self.chat_id))
            resp = requests.post(url, params=params)
            if resp.status_code != 200:
                logger.error("Error sending to telegram! Response: {0} {1}".format(resp.status_code, resp.content))
                return False                
            return True
        except Exception as e:
            logger.exception("Error sending telegram message! Error: %s", e)
            return False

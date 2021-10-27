import unittest, responses, re
from energymeter.telegram import telegram

class Test(unittest.TestCase):

    @responses.activate
    def test_send_ok(self):
        # Given    
        responses.add(responses.POST, re.compile('https://api.telegram.org/.*'), status=200)
        sender = telegram.Sender("123","456")

        # When
        resp = sender.send("Hallo Welt!")

        # Then
        assert resp == True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://api.telegram.org/bot123/sendMessage?chat_id=456&text=Hallo+Welt%21'

    def test_send_error(self):
        # Given    
        sender = telegram.Sender("123","456")

        # When
        resp = sender.send("Hallo Welt!")

        # Then
        assert resp == False
   
if __name__ == "__main__": 
    unittest.main()

from channels.generic.websocket import WebsocketConsumer
import json

class tableStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'tamos conectaos'
        }))
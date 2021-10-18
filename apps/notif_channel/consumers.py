import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class notificationConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("telegram_group", self.channel_name)
        self.accept()
       # async_to_sync(self.channel_layer.group_add)("telegram_notif", self.channel_name)


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("telegram_group", self.channel_name)
        pass

    def receive(self, text_data):
        #text_data_str = str(text_data)
        #text_data_json = json.loads(text_data)
        #message = text_data_json['message']
        #print(message)
        self.send(text_data=json.dumps({
            'message': text_data['text']
        }))
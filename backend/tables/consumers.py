from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .websocketService import tableStateNotification, ordersNotification
import json


class tableStatusConsumer(WebsocketConsumer):
    def connect(self):
        # Unirse al grupo que usa el emisor en websocketService.py
        self.group_name = 'tables'
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'tamos conectaos'
        }))

        # tableStateNotification()

    def disconnect(self, close_code):
        # Salir del grupo al desconectar
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    # Handler para eventos enviados con {'type': 'tables_actualization', 'datos': ...}
    def tables_actualization(self, event):
        self.send(text_data=json.dumps({
            'type': 'tables_actualization',
            'tables': event.get('datos')
        }))

class ordersConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'orders'
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        # user  = Aqui falta la logica de revisar los tokens de simpleJWT para obtener el user
        # if not user or not user.has_perm('view_orders'):
        #     self.close()
            # return 
        
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Conectado a órdenes'
        }))

        # ordersNotification() 

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
    
    def ordersActualization(self, event):

        self.send(text_data = json.dumps({
            'type': 'orders_actualization',
            'orders': event.get('datos')
        }))


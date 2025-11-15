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

        from .models import table
        from .serializers import tableSerializer
        tables = table.objects.all()
        serializer = tableSerializer(tables, many=True)
        self.send(json.dumps({
            'type': 'tablesActualization',
            'tables': serializer.data
        }))

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
     
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Conectado a órdenes'
        }))

        from .models import orderItem
        from .serializers import orderItemSerializer
        orderItem = orderItem.objects.all()
        serializer = orderItemSerializer(orderItem, many = True)

        self.send(text_data=json.dumps({
            'type': 'ordersActualization',
            'orders': serializer.data
        }))

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
    
    def ordersActualization(self, event):

        self.send(text_data = json.dumps({
            'type': 'ordersActualization',
            'orders': event.get('datos')
        }))


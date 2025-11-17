from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def tableStateNotification():
    from .models import table
    from .serializers import tableSerializer
    
    tables = table.objects.all()
    tablesData = tableSerializer(tables, many=True).data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'tables',
        {'type': 'tables_actualization', 'datos': tablesData}
    )

        
def ordersNotification():
    from .models import orderItem
    from .serializers import orderItemSerializer
    orders = order.objects.all()
    ordersData = orderSerializer(orders, many=True).data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'orders',
        {'type': 'ordersActualization', 'datos': ordersData}
    )
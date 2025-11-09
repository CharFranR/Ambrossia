from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import hashlib
from django.core.cache import cache

def tableStateNotification():
    from .models import table
    from .serializers import tableSerializer
    # primero creamos una tabla hash con los estados de las mesas 
    tables = list(table.objects.values('id', 'status').order_by('id'))
    hashTables = hashlib.md5(str(tables).encode()).hexdigest()

    # ahora comparamos la tabla hash actual con la guardad en caché
    # como la primera vez no hay caché se establece y manda el mensaje en automatico

    if hashTables != cache.get('tableStatus'):
        # entonces actualizamos la caché
        cache.set('tableStatus', hashTables)

        # la magia pues, mandamos el mensaje por el websocket

        tables = table.objects.all()
        tablesData = tableSerializer(tables, many=True).data

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'tables',
            {'type': 'tables_actualization', 'datos': tablesData}
        )

def ordersNotification():
    from .models import order
    from .serializers import orderSerializer
    orders = order.objects.all()
    ordersData = orderSerializer(orders, many=True).data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'orders',
        {'type': 'orders_actualization', 'datos': ordersData}
    )
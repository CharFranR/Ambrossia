from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import table
from .serializers import tableSerializer

# pues chapi me sopló la respuesta, me dijo que usara una tabla hash de los estados de la mesa y que 
# mandara un mensaje por websocket solo cuando el hash cambiara, porque originalmente pensaba solo actualizar
# el estado de las mesas cada segundo
import hashlib
from django.core.cache import cache


def tableStateNotification():
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
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import order, table
from .websocketService import tableStateNotification, ordersNotification
import logging

@receiver(post_save, sender = order)
def notifyOrderChange(sender, instance, created, **kwargs):
    try:
        ordersNotification()
    except Exception as e:
        logging.error(f"Error al enviar mensaje por websocket {e}")

@receiver(post_delete, sender = order)
def notifyOrderDelete(sender, instance, created, **kwargs):
    try: 
        ordersNotification()
    except Exception as e:
        logging.error(f"Error al enviar mensaje por wbeoscket {e}")

@receiver(post_save, sender = table)
def notifyTableChange(sender, instance, created, **kwargs):
    try:
        tableStateNotification()
    except Exception as e:
        logging.error(f"Error al enviar mensaje por websocket {e}")

@receiver(post_delete, sender = table)
def notifyTableDelete(sender, instance, created, **kwargs):
    try: 
        tableStateNotification()
    except Exception as e:
        logging.error(f"Error al enviar mensaje por wbeoscket {e}")
from django.db import models

class CustomUser(models.Model):
    class Meta:
        permissions = [
            ("mesero_access", "Acceso Mesero"),
            ("cocina_access", "Acceso Cocina"),
            ("caja_access", "Acceso Caja"),
            ("admin_access", "Acceso Administrador"),
        ]
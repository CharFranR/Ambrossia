# Guía de Refactorización del Backend

## Vista General

Este documento describe la refactorización completada para alinear todos los archivos `views.py` con la nueva estructura de modelos documentada en `docs/`.

## Declaración del Problema

Los modelos del backend fueron refactorizados para seguir una mejor estructura (separando encabezados de órdenes de items de órdenes, agregando relaciones apropiadas), pero todos los archivos `views.py` quedaron desactualizados e incompatibles con los nuevos modelos.

## Nueva Estructura de Modelos

### App Tables

**table** (Mesa)
- `id`: AutoField (clave primaria)
- `status`: CharField (available, occupied, reserved, in_cleaning)
- `tableNumber`: IntegerField

**order** (Encabezado de Orden)
- `id`: AutoField (clave primaria)
- `status`: CharField (notCooking, cooking, ready)
- `tableId`: ForeignKey a table
- `billId`: ForeignKey a bill (nullable - órdenes creadas antes de facturar)
- `createdAt`: DateTimeField (auto)
- `updatedAt`: DateTimeField (nullable)
- `waiterId`: IntegerField

**orderItem** (Items de la Orden)
- `id`: AutoField (clave primaria)
- `orderId`: ForeignKey a order
- `productId`: ForeignKey a product
- `quantity`: IntegerField
- `note`: TextField (opcional)

### App Menu

**productCategory** (Categoría de Producto)
- `id`: AutoField (clave primaria)
- `name`: CharField

**product** (Producto)
- `id`: AutoField (clave primaria)
- `name`: CharField
- `price`: IntegerField
- `categoryId`: ForeignKey a productCategory (nullable)

### App Bill

**bill** (Factura)
- `id`: AutoField (clave primaria)
- `status`: CharField (notPayed, payed)
- `tableId`: ForeignKey a table
- `createdAt`: DateTimeField (auto)
- `closedAt`: DateTimeField (nullable)
- `paidAmount`: FloatField (default: 0)
- `paymentMethod`: CharField (opcional)
- `cashier`: CharField (opcional)
- `IVA`: IntegerField (opcional, default: 0)
- `discount`: FloatField (opcional, default: 0)
- `total`: FloatField (default: 0)

## Cambios Realizados

### 1. tables/views.py

**Problema**: Las vistas intentaban crear objetos order planos con campos `product`, `quantity`, `note` que no existen en el nuevo modelo.

**Solución**:
- Actualizada la acción `add_order` para crear primero un encabezado de orden
- Luego crear instancias de orderItem para cada producto
- Agregado `OrderItemLegacySerializer` para mantener respuestas API retrocompatibles
- La API aún acepta `[{"product": id, "quantity": num, "note": "..."}]`
- Pero internamente crea order + orderItems

### 2. tables/serializers.py

**Agregado**:
- `OrderItemLegacySerializer`: Convierte el nuevo modelo orderItem al formato plano legacy
- Auto-genera `tableNumber` si no se proporciona en la creación de mesa
- Maneja valores por defecto para campos opcionales

### 3. menu/views.py

**Problema**: 
- Tenía ViewSets duplicados (ProductViewSet y ProductAdminViewSet)
- No manejaba el campo requerido `categoryId`

**Solución**:
- Fusionado en un único `ProductViewSet` con métodos create/update apropiados
- Auto-crea categoría por defecto si no se proporciona
- Agregado `ProductCategoryViewSet` para gestión de categorías
- Código simplificado usando defaults de ModelViewSet

### 4. bill/views.py

**Problema**: Referenciaba `order.quantity` y `order.product` que no existen en el nuevo modelo.

**Solución**:
- Actualizado `createBill` para iterar a través de órdenes y sus orderItems
- Calcula correctamente totales desde cantidades de orderItem y precios de productos
- Asocia órdenes con factura vía campo `billId`
- Genera PDF con estructura de datos correcta

### 5. users/views.py

**Problemas**:
- Faltaba parámetro `self` en métodos
- Usaba `get_object_or_404` en Token en lugar de `get_or_create`
- Errores de tipeo: `serializer.erros`, `serializer.save` (faltaban paréntesis)
- Los métodos no eran acciones apropiadas de ViewSet

**Solución**:
- Corregidos todos los errores de sintaxis
- Hecho `login` un endpoint `@action`
- Hecho `register` el método `create` estándar
- Agregada importación faltante de `Permission`
- Corregido formato de strings en respuestas

### 6. Actualizaciones de Modelos

Para soportar las nuevas vistas, se necesitaron cambios mínimos en los modelos:

**tables/models.py**:
- `order.billId`: Agregado `null=True, blank=True` (órdenes creadas antes de facturar)
- `orderItem.note`: Agregado `blank=True, default=''` (notas opcionales)

**menu/models.py**:
- `product.categoryId`: Agregado `null=True, blank=True` (categoría opcional)

**bill/models.py**:
- `paymentMethod`: Agregado `blank=True, default=''`
- `cashier`: Agregado `blank=True, default=''`
- Agregados defaults para IVA, discount, total

## Compatibilidad de API

La refactorización mantiene compatibilidad retroactiva con la API documentada en `docs/API/FrontendEndpoints.md`:

### Ejemplo: Creando Órdenes

**Request** (sin cambios):
```json
POST /tables/{table_id}/add_order/
[
  {"product": 1, "quantity": 2},
  {"product": 2, "quantity": 1, "note": "Sin cebolla"}
]
```

**Response** (formato sin cambios, nueva estructura interna):
```json
[
  {
    "id": 1,
    "table": 2,
    "product": 1,
    "quantity": 2,
    "status": "notCooking",
    "createdAt": "2025-11-04T01:36:27.734590Z",
    "closedAt": null,
    "note": ""
  },
  {
    "id": 2,
    "table": 2,
    "product": 2,
    "quantity": 1,
    "status": "notCooking",
    "createdAt": "2025-11-04T01:36:27.743490Z",
    "closedAt": null,
    "note": "Sin cebolla"
  }
]
```

Internamente, esto ahora crea:
1. Un objeto `order` (encabezado)
2. Dos objetos `orderItem` (items de línea)

## Migración Requerida

Los cambios en los modelos requieren migración de base de datos:

```bash
docker exec -it drf_backend python manage.py makemigrations
docker exec -it drf_backend python manage.py migrate
```

## Testing

Para probar los endpoints refactorizados:

```bash
# Iniciar los servicios
docker compose up -d

# Ejecutar suite de pruebas
cd backend/tests
python test_endpoints.py
```

## Trabajo Futuro

### Vistas Vacías Restantes

**inventory/views.py** y **cashRegister/views.py** están actualmente vacíos. Estos deberían implementarse basándose en:
- Estructura de inventory/models.py
- Estructura de cashRegister/models.py
- Requerimientos del negocio

### Mejoras Potenciales

1. **Agregar permisos apropiados**: Actualmente comentados, deberían habilitarse
2. **Agregar paginación**: Listas grandes deberían paginarse
3. **Agregar filtrado**: Permitir filtrar por fecha, estado, etc.
4. **Agregar validación**: Validación de entrada más robusta
5. **Manejo de errores**: Mejores mensajes de error y logging
6. **Tests**: Agregar pruebas unitarias para cada endpoint

## Convenciones

Siguiendo `docs/general/conventions.md`:

- Usar mensajes de commit descriptivos: `refactor(tables): actualizar vistas para nueva estructura de modelo`
- Nomenclatura de branches: `feature/`, `bugfix/`, `refactor/`
- Mantener PRs enfocados y pequeños
- Ejecutar migraciones antes de hacer push

## Solución de Problemas

### Problemas Comunes

1. **Errores "Field does not exist"**: Verificar que el modelo tiene el campo, ejecutar migraciones
2. **Errores de clave foránea**: Asegurar que los objetos relacionados existen antes de crear referencias
3. **Errores de validación**: Verificar que el serializer incluye todos los campos requeridos
4. **Errores de importación**: Verificar que se evitan imports circulares con referencias string ('app.Model')

### Tips de Debug

1. Revisar Django shell para probar queries:
```python
docker exec -it drf_backend python manage.py shell
>>> from tables.models import order, orderItem
>>> order.objects.all()
```

2. Verificar estado de migraciones:
```bash
docker exec -it drf_backend python manage.py showmigrations
```

3. Ver SQL siendo generado:
```python
>>> queryset = order.objects.filter(tableId=1)
>>> print(queryset.query)
```

## Resumen

Todos los archivos `views.py` han sido actualizados exitosamente para trabajar con los modelos refactorizados mientras mantienen compatibilidad retroactiva con la API documentada. Los cambios son mínimos, enfocados y preservan la funcionalidad existente.

## Pasos Siguientes Recomendados

1. **Ejecutar migraciones**: Aplicar los cambios de modelo a la base de datos
2. **Probar endpoints**: Verificar que todos los endpoints funcionan correctamente
3. **Revisar permisos**: Descomentar y configurar los permisos de usuario
4. **Implementar vistas faltantes**: inventory y cashRegister si son necesarias
5. **Agregar tests**: Crear pruebas unitarias para los nuevos cambios
6. **Documentar cambios**: Actualizar documentación de API si es necesario

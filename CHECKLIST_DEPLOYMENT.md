# Checklist para Despliegue Post-Refactorización

Esta checklist te guía a través de los pasos necesarios después de la refactorización del backend.

## ✅ Completado (por Copilot)

- [x] Actualizar todos los archivos `views.py`
- [x] Actualizar serializers para compatibilidad
- [x] Ajustar modelos (null/blank/defaults)
- [x] Corregir errores de sintaxis
- [x] Agregar imports faltantes
- [x] Verificar seguridad con CodeQL (0 alertas)
- [x] Crear documentación completa (EN/ES)
- [x] Crear archivo .env (gitignored)

## 🔄 Pendiente (Para Implementar)

### 1. Migraciones de Base de Datos ⚠️ CRÍTICO

```bash
# Iniciar servicios
docker compose up -d

# Crear migraciones
docker exec -it drf_backend python manage.py makemigrations

# Verificar migraciones
docker exec -it drf_backend python manage.py showmigrations

# Aplicar migraciones
docker exec -it drf_backend python manage.py migrate
```

**Esperado:** Migraciones para:
- `tables.order.billId` (null=True)
- `tables.orderItem.note` (default='')
- `menu.product.categoryId` (null=True)
- `bill.bill` (varios campos con defaults)

### 2. Testing Básico

```bash
# Test 1: Crear mesa
curl -X POST http://localhost:8000/tables/ -H "Content-Type: application/json"

# Test 2: Crear categoría
curl -X POST http://localhost:8000/category/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Bebidas"}'

# Test 3: Crear producto
curl -X POST http://localhost:8000/product/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Pizza", "price": 25, "categoryId": 1}'

# Test 4: Crear orden
curl -X POST http://localhost:8000/tables/1/add_order/ \
  -H "Content-Type: application/json" \
  -d '[{"product": 1, "quantity": 2}]'

# Test 5: Crear factura
curl -X POST http://localhost:8000/bills/createBill/1/ \
  -H "Content-Type: application/json"
```

### 3. Ejecutar Suite de Tests (si existe)

```bash
cd backend/tests
python test_endpoints.py
```

### 4. Revisión de Permisos

Los permisos están comentados en varios ViewSets:

```python
# En menu/views.py
# permission_classes = [IsMesero]

# En bill/views.py  
# permission_classes = [IsCaja]
```

**Acción:** Decidir si habilitar permisos ahora o después.

### 5. Implementaciones Opcionales

#### Inventory Views (si es necesario)
- Revisar `backend/inventory/models.py`
- Implementar `backend/inventory/views.py`
- Crear serializers
- Agregar URLs

#### CashRegister Views (si es necesario)
- Revisar `backend/cashRegister/models.py`
- Implementar `backend/cashRegister/views.py`
- Crear serializers
- Agregar URLs

### 6. Optimizaciones Futuras

- [ ] Agregar paginación a listados grandes
- [ ] Agregar filtrado por fecha/estado
- [ ] Optimizar queries con select_related
- [ ] Agregar logging comprehensivo
- [ ] Implementar rate limiting
- [ ] Agregar cache donde sea apropiado

### 7. Testing Comprehensivo

- [ ] Tests unitarios para cada ViewSet
- [ ] Tests de integración para flujos completos
- [ ] Tests de permisos
- [ ] Tests de validación de datos
- [ ] Tests de manejo de errores

### 8. Monitoreo y Logs

- [ ] Configurar logging centralizado
- [ ] Agregar métricas de performance
- [ ] Configurar alertas para errores
- [ ] Monitorear uso de base de datos

## 📋 Verificación Post-Deployment

### API Endpoints a Verificar

- [ ] `GET /tables/` - Listar mesas
- [ ] `POST /tables/` - Crear mesa
- [ ] `GET /tables/{id}/` - Detalle de mesa
- [ ] `PUT /tables/{id}/update_status/` - Actualizar estado
- [ ] `POST /tables/{id}/add_order/` - Crear orden
- [ ] `GET /product/` - Listar productos
- [ ] `POST /product/` - Crear producto
- [ ] `PUT /product/{id}/` - Actualizar producto
- [ ] `GET /category/` - Listar categorías
- [ ] `POST /category/` - Crear categoría
- [ ] `POST /bills/createBill/{table_id}/` - Crear factura
- [ ] `GET /bills/getNotPayedBills/` - Facturas no pagadas
- [ ] `GET /bills/getPayedBills/` - Facturas pagadas
- [ ] `PUT /bills/updateBill/{id}/` - Actualizar factura
- [ ] `PUT /bills/updateBillStatus/{id}/` - Actualizar estado
- [ ] `POST /users/` - Registrar usuario
- [ ] `POST /users/login/` - Login usuario
- [ ] `POST /api/token/` - Obtener JWT token
- [ ] `POST /api/token/refresh/` - Refrescar token

### Base de Datos a Verificar

```sql
-- Verificar estructura de tablas
\d tables_table
\d tables_order
\d tables_orderitem
\d menu_product
\d menu_productcategory
\d bill_bill

-- Verificar que las relaciones existen
SELECT * FROM tables_order WHERE id = 1;
SELECT * FROM tables_orderitem WHERE orderId_id = 1;
```

### Logs a Revisar

```bash
# Logs del contenedor
docker logs drf_backend

# Logs en tiempo real
docker logs -f drf_backend
```

## 🚨 Problemas Comunes y Soluciones

### Error: "Field does not exist"
**Causa:** Migraciones no aplicadas
**Solución:** Ejecutar `python manage.py migrate`

### Error: "Cannot assign None to field"
**Causa:** Intentando crear registro con campo requerido vacío
**Solución:** Verificar que campos opcionales tienen null=True o default

### Error: "No such table"
**Causa:** Base de datos no inicializada
**Solución:** Ejecutar migraciones desde cero

### Error: "Circular import"
**Causa:** Imports incorrectos entre apps
**Solución:** Usar referencias string en ForeignKey

### Error 500 en endpoints
**Causa:** Ver logs del backend
**Solución:** `docker logs drf_backend` para detalles

## 📚 Documentación de Referencia

- **REFACTORING_GUIDE.md**: Guía técnica completa (EN)
- **GUIA_REFACTORIZACION.md**: Guía completa (ES)
- **REFACTORING_SUMMARY.md**: Resumen ejecutivo
- **docs/API/FrontendEndpoints.md**: Documentación de API

## ✅ Checklist Final

Antes de considerar el deployment completo:

- [ ] Migraciones ejecutadas exitosamente
- [ ] Todos los endpoints básicos funcionan
- [ ] Tests pasan (si existen)
- [ ] Logs no muestran errores críticos
- [ ] Frontend puede consumir la API
- [ ] Documentación actualizada
- [ ] Equipo notificado de cambios

## 🎉 Conclusión

Una vez completados estos pasos, la refactorización estará completamente implementada y el backend estará funcionando con la nueva estructura de modelos.

Para preguntas o problemas, consultar las guías de refactorización detalladas.

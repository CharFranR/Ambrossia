# Documentación de Endpoints del Backend (para Frontend)

Esta guía resume todos los endpoints disponibles, qué hacen y ejemplos de los JSON que reciben y responden.

- Base URL (desarrollo): `http://localhost:8000`
- Formato: `application/json`
- Las rutas usan barra final `/` (importante en Django REST).
- No hay autenticación en este proyecto (a la fecha).

## Productos (Menú)

### 1) Crear producto

- Método y ruta: `POST /product/`

- Descripción: Crea un nuevo producto del menú.

- Body (JSON):

```json
{
  "name": "Pizza",
  "price": 25
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Pizza",
  "price": 25
}
```

- Errores comunes:
  - 400 si faltan campos requeridos o tipos inválidos.

### 2) Listar productos

- Método y ruta: `GET /Products/All`

- Descripción: Obtiene todos los productos.

- Respuesta 200 (JSON):

```json
[
  { "id": 1, "name": "Pizza", "price": 25 },
  { "id": 2, "name": "Refresco", "price": 10 }
]
```

### 3) Actualizar producto

- Método y ruta: `PUT /product/{id}/`

- Descripción: Actualización parcial de `name` y/o `price`.

- Body (JSON, cualquiera de los campos):

```json
{
  "name": "Pizza grande",
  "price": 30
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Pizza grande",
  "price": 30
}
```

- Errores comunes:
  - 404 si el `id` no existe.

---

## Mesas y Pedidos

### 4) Crear mesa

- Método y ruta: `POST /tables/`

- Descripción: Crea una mesa nueva en estado `available`.

- Body: vacío

- Respuesta 200 (JSON):

```json
{
  "id": 10,
  "status": "available"
}
```

### 5) Obtener estado de una mesa

- Método y ruta: `GET /tables/{id}/`

- Descripción: Retorna el estado de la mesa (`available`, `occupied`, `reserved`, `in_cleaning`).

- Respuesta 200 (JSON):

```json
{
  "id": 10,
  "status": "available"
}
```

- Errores comunes:
  - 404 si la mesa no existe.

### 6) Actualizar estado de una mesa

- Método y ruta: `PUT /tables/{id}/`

- Descripción: Cambia el estado de la mesa.

- Body (JSON):

```json
{
  "new_status": "reserved"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 10,
  "status": "reserved"
}
```

- Errores comunes:
  - 404 si la mesa no existe.

### 7) Crear pedido (order) para una mesa

- Método y ruta: `POST /tables/{table_id}/orders/`

- Descripción: Crea una orden asociada a la mesa. La mesa pasa a estado `occupied`.

- Body (JSON):

```json

[
  {
    "product": 1,
    "quantity": 2
  },
  {
    "product": 2,
    "quantity": 2
  }
]

```

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "table": 2,
    "product": 1,
    "status": "notCooking",
    "createdAt": "2025-11-04T01:36:27.734590Z",
    "closedAt": null,
    "note": ""
  },
  {
    "id": 2,
    "table": 2,
    "product": 2,
    "status": "notCooking",
    "createdAt": "2025-11-04T01:36:27.743490Z",
    "closedAt": null,
    "note": ""
  }
]
```

- Errores comunes:
  - 400 si `product` no existe o el body es inválido.
  - 404 si `table_id` no existe.

---

## Facturación (Bills)

### 8) Crear factura para una mesa

- Método y ruta: `POST /tables/{table_id}/bills/`

- Descripción: Crea una factura que agrupa todas las órdenes de la mesa que aún no tienen factura.

- Body: vacío

- Respuesta 200 (JSON):

```json
{
  "id": 3,
  "status": "notPayed",
  "createdAt": "2025-11-01T20:20:00Z",
  "closedAt": null,
  "orders": [5, 6]
}
```

- Errores comunes:
  - 400 si la mesa no tiene órdenes pendientes de facturar.
  - 404 si `table_id` no existe.

### 9) Actualizar estado de una factura

- Método y ruta: `PUT /bills/{bill_id}/status/`

- Descripción: Cambia el estado de la factura a `notPayed` o `payed`.

- Body (JSON):

```json
{
  "status": "payed"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 3,
  "status": "payed",
  "createdAt": "2025-11-01T20:20:00Z",
  "closedAt": null,
  "orders": [5, 6]
}
```

- Errores comunes:
  - 400 si `status` no es válido.
  - 404 si `bill_id` no existe.

### 10) Listar facturas no pagadas

- Método y ruta: `GET /bills/not-payed/`

- Descripción: Lista las facturas con estado `notPayed`.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 3,
    "status": "notPayed",
    "createdAt": "2025-11-01T20:20:00Z",
    "closedAt": null,
    "orders": [5, 6]
  }
]
```

### 11) Listar facturas pagadas

- Método y ruta: `GET /bills/payed/`

- Descripción: Lista las facturas con estado `payed`.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 4,
    "status": "payed",
    "createdAt": "2025-11-01T20:30:00Z",
    "closedAt": null,
    "orders": [7]
  }
]
```

---

## Notas útiles para Frontend

- En desarrollo, el backend corre en `http://localhost:8000` (Docker: `docker compose up -d`).
- Todos los endpoints responden JSON; usar encabezado `Content-Type: application/json` en solicitudes con cuerpo.
- Estados válidos:
  - Mesa: `available`, `occupied`, `reserved`, `in_cleaning`.
  - Factura: `notPayed`, `payed`.
- Las órdenes incluyen: `id`, `table`, `product`, `status`, `createdAt`, `closedAt`, `note`.

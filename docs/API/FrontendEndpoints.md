# Documentación de Endpoints del Backend (para Frontend)

Esta guía documenta todos los endpoints disponibles del backend de Ambrossia, con ejemplos de las peticiones y respuestas en formato JSON.

- Base URL (desarrollo): `http://localhost:8000`
- Formato: `application/json`
- Las rutas usan barra final `/` (importante en Django REST Framework)

---

## Autenticación (JWT)

### 1) Obtener token JWT
Método y ruta: POST /api/token/

Descripción: Genera tokens de acceso y refresco para autenticación.

Body (JSON):
{
  "username": "usuario",
  "password": "contraseña"
}

Respuesta 200 (JSON):
{
  "refresh": "...",
  "access": "..."
}

### 2) Refrescar token JWT
Método y ruta: POST /api/token/refresh/

Descripción: Genera un nuevo token de acceso usando el token de refresco.

Body (JSON):
{
  "refresh": "..."
}

Respuesta 200 (JSON):
{
  "access": "..."
}

---

## Usuarios

### 3) Registrar usuario
Método y ruta: POST /users/register/

Descripción: Crea un nuevo usuario y devuelve un token de autenticación.

Body (JSON):
{
  "username": "nuevo",
  "password": "secreta",
  "role": "mesero"
}

Respuesta 201 (JSON):
{
  "token": "...",
  "user": {
    "username": "nuevo",
    "id": 1
  }
}

### 4) Login usuario
Método y ruta: POST /users/login/

Descripción: Autentica un usuario existente y devuelve un token.

Body (JSON):
{
  "username": "usuario",
  "password": "secreta"
}

Respuesta 200 (JSON):
{
  "token": "...",
  "user": {
    "username": "usuario",
    "id": 1
  }
}

---

## Productos (Menú)

### 5) Crear producto
Método y ruta: POST /product/

Descripción: Crea un nuevo producto del menú.

Body (JSON):
{
  "name": "Pizza Margarita",
  "price": 250,
  "categoryId": 1
}

Respuesta 201 (JSON):
{
  "id": 1,
  "name": "Pizza Margarita",
  "price": 250,
  "categoryId": 1
}

### 6) Listar todos los productos
Método y ruta: GET /product/

Descripción: Obtiene todos los productos del menú.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "name": "Pizza Margarita",
    "price": 250,
    "categoryId": 1
  },
  {
    "id": 2,
    "name": "Refresco",
    "price": 35,
    "categoryId": 2
  }
]

### 7) Obtener todos los productos (método alternativo)
Método y ruta: GET /product/get_all_products/

Descripción: Obtiene todos los productos disponibles en el menú.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "name": "Pizza Margarita",
    "price": 250,
    "categoryId": 1
  }
]

### 8) Obtener productos por categoría
Método y ruta: GET /product/get_by_category/?categoryId={category_id}

Descripción: Filtra productos por ID de categoría.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "name": "Pizza Margarita",
    "price": 250,
    "categoryId": 1
  }
]

### 9) Obtener un producto específico
Método y ruta: GET /product/{id}/

Descripción: Obtiene los detalles de un producto específico.

Respuesta 200 (JSON):
{
  "id": 1,
  "name": "Pizza Margarita",
  "price": 250,
  "categoryId": 1
}

### 10) Actualizar producto
Método y ruta: PUT /product/{id}/

Descripción: Actualiza los datos de un producto existente (actualización parcial permitida).

Body (JSON):
{
  "name": "Pizza Grande",
  "price": 300
}

Respuesta 200 (JSON):
{
  "id": 1,
  "name": "Pizza Grande",
  "price": 300,
  "categoryId": 1
}

### 11) Eliminar producto
Método y ruta: DELETE /product/{id}/

Descripción: Elimina un producto del menú.

Respuesta 204 (sin contenido)

---

## Mesas

### 12) Crear mesa
Método y ruta: POST /api/tables/

Descripción: Crea una nueva mesa con estado "available".

Body (JSON):
{
  "tableNumber": 10
}

Respuesta 201 (JSON):
{
  "id": 1,
  "status": "available",
  "tableNumber": 10
}

### 13) Listar todas las mesas
Método y ruta: GET /api/tables/

Descripción: Obtiene todas las mesas del restaurante.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "status": "available",
    "tableNumber": 10
  },
  {
    "id": 2,
    "status": "occupied",
    "tableNumber": 5
  }
]

### 14) Obtener estado de una mesa
Método y ruta: GET /api/tables/{id}/

Descripción: Obtiene el estado y datos de una mesa específica.

Respuesta 200 (JSON):
{
  "id": 1,
  "status": "available",
  "tableNumber": 10
}

### 15) Actualizar estado de una mesa
Método y ruta: PUT /api/tables/{id}/update_status/

Descripción: Cambia el estado de la mesa. Estados válidos: available, occupied, reserved, in_cleaning.

Body (JSON):
{
  "status": "reserved"
}

Respuesta 200 (JSON):
{
  "id": 1,
  "status": "reserved",
  "tableNumber": 10
}

---

## Órdenes

### 16) Crear orden
Método y ruta: POST /api/orders/

Descripción: Crea una nueva orden asociada a una mesa.

Body (JSON):
{
  "tableId": 1,
  "waiterId": 5,
  "status": "notCooking"
}

Respuesta 201 (JSON):
{
  "id": 1,
  "tableId": 1,
  "waiterId": 5,
  "status": "notCooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": null,
  "billId": null
}

### 17) Listar todas las órdenes
Método y ruta: GET /api/orders/

Descripción: Obtiene todas las órdenes del sistema.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "tableId": 1,
    "waiterId": 5,
    "status": "notCooking",
    "createdAt": "2025-11-13T20:00:00Z",
    "updatedAt": null,
    "billId": null
  }
]

### 18) Obtener una orden específica
Método y ruta: GET /api/orders/{id}/

Descripción: Obtiene los detalles de una orden específica.

Respuesta 200 (JSON):
{
  "id": 1,
  "tableId": 1,
  "waiterId": 5,
  "status": "notCooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": null,
  "billId": null
}

### 19) Actualizar orden
Método y ruta: PUT /api/orders/{id}/

Descripción: Actualiza los datos de una orden (actualización parcial permitida).

Body (JSON):
{
  "status": "cooking",
  "waiterId": 3
}

Respuesta 200 (JSON):
{
  "id": 1,
  "tableId": 1,
  "waiterId": 3,
  "status": "cooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": "2025-11-13T20:10:00Z",
  "billId": null
}

### 20) Actualizar estado de una orden
Método y ruta: PUT /api/orders/{id}/update_status/

Descripción: Cambia el estado de una orden. Estados válidos: notCooking, cooking, ready.

Body (JSON):
{
  "status": "cooking"
}

Respuesta 200 (JSON):
{
  "id": 1,
  "tableId": 1,
  "waiterId": 5,
  "status": "cooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": "2025-11-13T20:10:00Z",
  "billId": null
}

### 21) Obtener items de una orden
Método y ruta: GET /api/orders/{id}/get_items/

Descripción: Lista todos los items (productos) de una orden específica.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "orderId": 1,
    "productId": 1,
    "quantity": 2,
    "note": "Sin cebolla"
  },
  {
    "id": 2,
    "orderId": 1,
    "productId": 3,
    "quantity": 1,
    "note": ""
  }
]

### 22) Agregar item a una orden
Método y ruta: POST /api/orders/{id}/add_item/

Descripción: Agrega un producto (item) a una orden existente.

Body (JSON):
{
  "productId": 1,
  "quantity": 2,
  "note": "Sin cebolla"
}

Respuesta 201 (JSON):
{
  "id": 1,
  "orderId": 1,
  "productId": 1,
  "quantity": 2,
  "note": "Sin cebolla"
}

### 23) Eliminar orden
Método y ruta: DELETE /api/orders/{id}/

Descripción: Elimina una orden del sistema.

Respuesta 204 (sin contenido)

---

## Facturación (Bills)

### 24) Crear factura para una mesa
Método y ruta: POST /bills/create_bill/{table_id}/

Descripción: Crea una factura agrupando todas las órdenes de la mesa que no tienen factura. Calcula automáticamente IVA (15%) y total.

Body (JSON):
{
  "cashier": "Juan Pérez",
  "paymentMethod": "cash",
  "discount": 0
}

Respuesta 201 (JSON):
{
  "bill": {
    "id": 1,
    "status": "notPayed",
    "tableId": 1,
    "createdAt": "2025-11-13T20:30:00Z",
    "closedAt": null,
    "paidAmount": 500.0,
    "paymentMethod": "cash",
    "cashier": "Juan Pérez",
    "IVA": 75.0,
    "discount": 0.0,
    "total": 575.0
  },
  "orders": [
    {
      "product": "Pizza Margarita",
      "price": 250,
      "quantity": 2,
      "amount": 500
    }
  ]
}

### 25) Listar todas las facturas
Método y ruta: GET /bills/

Descripción: Obtiene todas las facturas del sistema.

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "status": "notPayed",
    "tableId": 1,
    "createdAt": "2025-11-13T20:30:00Z",
    "closedAt": null,
    "paidAmount": 500.0,
    "paymentMethod": "cash",
    "cashier": "Juan Pérez",
    "IVA": 75.0,
    "discount": 0.0,
    "total": 575.0
  }
]

### 26) Obtener una factura específica
Método y ruta: GET /bills/{id}/

Descripción: Obtiene los detalles de una factura específica.

Respuesta 200 (JSON):
{
  "id": 1,
  "status": "notPayed",
  "tableId": 1,
  "createdAt": "2025-11-13T20:30:00Z",
  "closedAt": null,
  "paidAmount": 500.0,
  "paymentMethod": "cash",
  "cashier": "Juan Pérez",
  "IVA": 75.0,
  "discount": 0.0,
  "total": 575.0
}

### 27) Listar facturas no pagadas
Método y ruta: GET /bills/get_not_payed_bills/

Descripción: Lista todas las facturas con estado "notPayed".

Respuesta 200 (JSON):
[
  {
    "id": 1,
    "status": "notPayed",
    "tableId": 1,
    "createdAt": "2025-11-13T20:30:00Z",
    "closedAt": null,
    "paidAmount": 500.0,
    "paymentMethod": "cash",
    "cashier": "Juan Pérez",
    "IVA": 75.0,
    "discount": 0.0,
    "total": 575.0
  }
]

### 28) Listar facturas pagadas
Método y ruta: GET /bills/get_payed_bills/

Descripción: Lista todas las facturas con estado "payed".

Respuesta 200 (JSON):
[
  {
    "id": 2,
    "status": "payed",
    "tableId": 2,
    "createdAt": "2025-11-13T19:00:00Z",
    "closedAt": "2025-11-13T19:30:00Z",
    "paidAmount": 350.0,
    "paymentMethod": "card",
    "cashier": "María López",
    "IVA": 52.5,
    "discount": 35.0,
    "total": 367.5
  }
]

### 29) Actualizar valores de una factura
Método y ruta: PUT /bills/{id}/update_bill/

Descripción: Actualiza IVA y descuento de una factura. Solo se puede modificar si no está pagada.

Body (JSON):
{
  "IVA": 15,
  "discount": 50
}

Respuesta 200 (JSON):
{
  "id": 1,
  "status": "notPayed",
  "tableId": 1,
  "createdAt": "2025-11-13T20:30:00Z",
  "closedAt": null,
  "paidAmount": 500.0,
  "paymentMethod": "cash",
  "cashier": "Juan Pérez",
  "IVA": 75.0,
  "discount": 50.0,
  "total": 525.0
}

### 30) Actualizar estado de una factura
Método y ruta: PUT /bills/{id}/update_status/

Descripción: Cambia el estado de pago de una factura. Estados válidos: notPayed, payed.

Body (JSON):
{
  "status": "payed"
}

Respuesta 200 (JSON):
{
  "id": 1,
  "status": "payed",
  "tableId": 1,
  "createdAt": "2025-11-13T20:30:00Z",
  "closedAt": "2025-11-13T20:45:00Z",
  "paidAmount": 500.0,
  "paymentMethod": "cash",
  "cashier": "Juan Pérez",
  "IVA": 75.0,
  "discount": 0.0,
  "total": 575.0
}

### 31) Eliminar factura
Método y ruta: DELETE /bills/{id}/

Descripción: Elimina una factura del sistema.

Respuesta 204 (sin contenido)

---

## Notas útiles para Frontend

- **Base URL de desarrollo**: `http://localhost:8000`
- **Contenido**: Todos los endpoints esperan y responden JSON. Usar header `Content-Type: application/json`.
- **Barras finales**: Django REST Framework requiere `/` al final de las rutas.
- **Estados válidos**:
  - Mesa: `available`, `occupied`, `reserved`, `in_cleaning`
  - Orden: `notCooking`, `cooking`, `ready`
  - Factura: `notPayed`, `payed`
- **Autenticación**: Usar tokens JWT en header `Authorization: Bearer {token}`
- **Roles de usuario**: `mesero`, `cocina`, `caja`, `admin`

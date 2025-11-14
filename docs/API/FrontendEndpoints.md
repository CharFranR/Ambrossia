# Documentación de Endpoints del Backend (para Frontend)

Esta guía documenta todos los endpoints disponibles del backend de Ambrossia, con ejemplos de las peticiones y respuestas en formato JSON.

- Base URL (desarrollo): `http://localhost:8000`
- Formato: `application/json`
- Las rutas usan barra final `/` (importante en Django REST Framework)

---

## Autenticación (JWT)

### 1) Obtener token JWT

- Método y ruta: `POST /api/token/`

- Descripción: Genera tokens de acceso y refresco para autenticación.

- Body (JSON):

```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

- Respuesta 200 (JSON):

```json
{
  "refresh": "...",
  "access": "..."
}
```

### 2) Refrescar token JWT

- Método y ruta: `POST /api/token/refresh/`

- Descripción: Genera un nuevo token de acceso usando el token de refresco.

- Body (JSON):

```json
{
  "refresh": "..."
}
```

- Respuesta 200 (JSON):

```json
{
  "access": "..."
}
```

---

## Usuarios

### 3) Registrar usuario

- Método y ruta: `POST /users/register/`

- Descripción: Crea un nuevo usuario y devuelve un token de autenticación.

- Body (JSON):

```json
{
  "username": "nuevo",
  "password": "secreta",
  "role": "mesero"
}
```

- Respuesta 201 (JSON):

```json
{
  "token": "...",
  "user": {
    "username": "nuevo",
    "id": 1
  }
}
```

### 4) Login usuario

- Método y ruta: `POST /users/login/`

- Descripción: Autentica un usuario existente y devuelve un token.

- Body (JSON):

```json
{
  "username": "usuario",
  "password": "secreta"
}
```

- Respuesta 200 (JSON):

```json
{
  "token": "...",
  "user": {
    "username": "usuario",
    "id": 1
  }
}
```

---

## Categorías de Productos

### 5) Crear categoría

- Método y ruta: `POST /productCategory/`

- Descripción: Crea una nueva categoría de productos.

- Body (JSON):

```json
{
  "name": "Bebidas"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "name": "Bebidas"
}
```

### 6) Listar todas las categorías

- Método y ruta: `GET /productCategory/`

- Descripción: Obtiene todas las categorías de productos.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "name": "Bebidas"
  },
  {
    "id": 2,
    "name": "Pizzas"
  }
]
```

### 7) Obtener una categoría específica

- Método y ruta: `GET /productCategory/{id}/`

- Descripción: Obtiene los detalles de una categoría específica.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Bebidas"
}
```

### 8) Agregar categoría (método alternativo)

- Método y ruta: `POST /productCategory/add_category/`

- Descripción: Crea una nueva categoría de productos (método alternativo).

- Body (JSON):

```json
{
  "name": "Postres"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 3,
  "name": "Postres"
}
```

### 9) Actualizar categoría

- Método y ruta: `PUT /productCategory/{id}/update_category/`

- Descripción: Actualiza los datos de una categoría existente.

- Body (JSON):

```json
{
  "name": "Bebidas Frías"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Bebidas Frías"
}
```

### 10) Eliminar categoría

- Método y ruta: `DELETE /productCategory/{id}/delete_category/`

- Descripción: Elimina una categoría del sistema.

- Respuesta 200 (JSON):

```json
{
  "message": "Categoría eliminada correctamente"
}
```

---

## Productos (Menú)

### 11) Crear producto

- Método y ruta: `POST /product/`

- Descripción: Crea un nuevo producto del menú.

- Body (JSON):

```json
{
  "name": "Pizza Margarita",
  "price": 250,
  "categoryId": 1
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "name": "Pizza Margarita",
  "price": 250,
  "categoryId": 1
}
```

### 12) Listar todos los productos

- Método y ruta: `GET /product/`

- Descripción: Obtiene todos los productos del menú.

- Respuesta 200 (JSON):

```json
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
```

### 13) Obtener todos los productos (método alternativo)

- Método y ruta: `GET /product/get_all_products/`

- Descripción: Obtiene todos los productos disponibles en el menú.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "name": "Pizza Margarita",
    "price": 250,
    "categoryId": 1
  }
]
```

### 14) Obtener productos por categoría

- Método y ruta: `GET /product/get_by_category/?categoryId={category_id}`

- Descripción: Filtra productos por ID de categoría.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "name": "Pizza Margarita",
    "price": 250,
    "categoryId": 1
  }
]
```

### 15) Obtener un producto específico

- Método y ruta: `GET /product/{id}/`

- Descripción: Obtiene los detalles de un producto específico.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Pizza Margarita",
  "price": 250,
  "categoryId": 1
}
```

### 16) Actualizar producto

- Método y ruta: `PUT /product/{id}/`

- Descripción: Actualiza los datos de un producto existente (actualización parcial permitida).

- Body (JSON):

```json
{
  "name": "Pizza Grande",
  "price": 300
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Pizza Grande",
  "price": 300,
  "categoryId": 1
}
```

### 17) Eliminar producto

- Método y ruta: `DELETE /product/{id}/`

- Descripción: Elimina un producto del menú.

- Respuesta 204 (sin contenido)

---

## Recetas (Cookbook)

### 18) Crear receta

- Método y ruta: `POST /Cookbook/`

- Descripción: Crea una nueva receta en el libro de cocina.

- Body (JSON):

```json
{
  "name": "Pizza Margarita Casera",
  "note": "Receta tradicional italiana con masa artesanal"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "name": "Pizza Margarita Casera",
  "note": "Receta tradicional italiana con masa artesanal"
}
```

### 19) Listar todas las recetas

- Método y ruta: `GET /Cookbook/`

- Descripción: Obtiene todas las recetas del libro de cocina.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "name": "Pizza Margarita Casera",
    "note": "Receta tradicional italiana con masa artesanal"
  },
  {
    "id": 2,
    "name": "Pasta Carbonara",
    "note": "Receta romana clásica"
  }
]
```

### 20) Obtener una receta específica

- Método y ruta: `GET /Cookbook/{id}/`

- Descripción: Obtiene los detalles de una receta específica.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Pizza Margarita Casera",
  "note": "Receta tradicional italiana con masa artesanal"
}
```

### 21) Actualizar receta

- Método y ruta: `PUT /Cookbook/{id}/`

- Descripción: Actualiza los datos de una receta existente (actualización parcial permitida).

- Body (JSON):

```json
{
  "name": "Pizza Margarita Premium",
  "note": "Receta con ingredientes premium"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Pizza Margarita Premium",
  "note": "Receta con ingredientes premium"
}
```

### 22) Eliminar receta

- Método y ruta: `DELETE /Cookbook/{id}/`

- Descripción: Elimina una receta del libro de cocina.

- Respuesta 204 (sin contenido)

### 23) Obtener ingredientes de una receta

- Método y ruta: `GET /Cookbook/{id}/get_ingredients/`

- Descripción: Lista todos los ingredientes asociados a una receta específica.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "recipe": 1,
    "ingredient": 5
  },
  {
    "id": 2,
    "recipe": 1,
    "ingredient": 8
  }
]
```

---

## Ingredientes

### 24) Crear ingrediente

- Método y ruta: `POST /Ingredient/`

- Descripción: Crea un nuevo ingrediente en el sistema.

- Body (JSON):

```json
{
  "name": "Harina de trigo",
  "unit": "kg"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "name": "Harina de trigo",
  "unit": "kg"
}
```

### 25) Listar todos los ingredientes

- Método y ruta: `GET /Ingredient/`

- Descripción: Obtiene todos los ingredientes disponibles.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "name": "Harina de trigo",
    "unit": "kg"
  },
  {
    "id": 2,
    "name": "Tomate",
    "unit": "unidad"
  }
]
```

### 26) Obtener un ingrediente específico

- Método y ruta: `GET /Ingredient/{id}/`

- Descripción: Obtiene los detalles de un ingrediente específico.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Harina de trigo",
  "unit": "kg"
}
```

### 27) Actualizar ingrediente

- Método y ruta: `PUT /Ingredient/{id}/`

- Descripción: Actualiza los datos de un ingrediente existente (actualización parcial permitida).

- Body (JSON):

```json
{
  "name": "Harina de trigo integral",
  "unit": "kg"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "name": "Harina de trigo integral",
  "unit": "kg"
}
```

### 28) Eliminar ingrediente

- Método y ruta: `DELETE /Ingredient/{id}/`

- Descripción: Elimina un ingrediente del sistema.

- Respuesta 204 (sin contenido)

### 29) Agregar ingrediente (método alternativo)

- Método y ruta: `POST /Ingredient/add_ingredient/`

- Descripción: Crea un nuevo ingrediente en el sistema (método alternativo).

- Body (JSON):

```json
{
  "name": "Queso mozzarella",
  "unit": "kg"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 3,
  "name": "Queso mozzarella",
  "unit": "kg"
}
```

### 30) Actualizar ingrediente (método alternativo)

- Método y ruta: `PUT /Ingredient/{id}/update_ingredient/`

- Descripción: Actualiza los datos de un ingrediente existente (método alternativo).

- Body (JSON):

```json
{
  "name": "Queso mozzarella premium",
  "unit": "kg"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 3,
  "name": "Queso mozzarella premium",
  "unit": "kg"
}
```

### 31) Eliminar ingrediente (método alternativo)

- Método y ruta: `DELETE /Ingredient/{id}/delete_ingredient/`

- Descripción: Elimina un ingrediente del sistema (método alternativo).

- Respuesta 200 (JSON):

```json
{
  "message": "Ingrediente eliminado correctamente"
}
```

---

## Ingredientes de Receta (CookbookIngredient)

### 32) Crear relación receta-ingrediente

- Método y ruta: `POST /CookbookIngredient/`

- Descripción: Asocia un ingrediente a una receta del libro de cocina.

- Body (JSON):

```json
{
  "recipe": 1,
  "ingredient": 5
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "recipe": 1,
  "ingredient": 5
}
```

### 33) Listar todas las relaciones receta-ingrediente

- Método y ruta: `GET /CookbookIngredient/`

- Descripción: Obtiene todas las relaciones entre recetas e ingredientes.

- Respuesta 200 (JSON):

```json
[
  {
    "id": 1,
    "recipe": 1,
    "ingredient": 5
  },
  {
    "id": 2,
    "recipe": 1,
    "ingredient": 8
  }
]
```

### 34) Obtener una relación específica

- Método y ruta: `GET /CookbookIngredient/{id}/`

- Descripción: Obtiene los detalles de una relación receta-ingrediente específica.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "recipe": 1,
  "ingredient": 5
}
```

### 35) Actualizar relación receta-ingrediente

- Método y ruta: `PUT /CookbookIngredient/{id}/`

- Descripción: Actualiza una relación entre receta e ingrediente (actualización parcial permitida).

- Body (JSON):

```json
{
  "recipe": 2,
  "ingredient": 5
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "recipe": 2,
  "ingredient": 5
}
```

### 36) Eliminar relación receta-ingrediente

- Método y ruta: `DELETE /CookbookIngredient/{id}/`

- Descripción: Elimina una relación entre receta e ingrediente.

- Respuesta 204 (sin contenido)

### 37) Agregar ingrediente a receta (método alternativo)

- Método y ruta: `POST /CookbookIngredient/add_cookbook_ingredient/`

- Descripción: Asocia un ingrediente a una receta (método alternativo).

- Body (JSON):

```json
{
  "recipe": 1,
  "ingredient": 10
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 3,
  "recipe": 1,
  "ingredient": 10
}
```

### 38) Actualizar ingrediente de receta (método alternativo)

- Método y ruta: `PUT /CookbookIngredient/{id}/update_cookbook_ingredient/`

- Descripción: Actualiza una relación entre receta e ingrediente (método alternativo).

- Body (JSON):

```json
{
  "recipe": 2,
  "ingredient": 12
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 3,
  "recipe": 2,
  "ingredient": 12
}
```

### 39) Eliminar ingrediente de receta (método alternativo)

- Método y ruta: `DELETE /CookbookIngredient/{id}/delete_cookbook_ingredient/`

- Descripción: Elimina una relación entre receta e ingrediente (método alternativo).

- Respuesta 200 (JSON):

```json
{
  "message": "Relación eliminada correctamente"
}
```

---

## Mesas

### 40) Crear mesa

- Método y ruta: `POST /api/tables/`

- Descripción: Crea una nueva mesa con estado "available".

- Body (JSON):

```json
{
  "tableNumber": 10
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "status": "available",
  "tableNumber": 10
}
```

### 41) Listar todas las mesas

- Método y ruta: `GET /api/tables/`

- Descripción: Obtiene todas las mesas del restaurante.

- Respuesta 200 (JSON):

```json
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
```

### 42) Obtener estado de una mesa

- Método y ruta: `GET /api/tables/{id}/`

- Descripción: Obtiene el estado y datos de una mesa específica.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "status": "available",
  "tableNumber": 10
}
```

### 43) Actualizar estado de una mesa

- Método y ruta: `PUT /api/tables/{id}/update_status/`

- Descripción: Cambia el estado de la mesa. Estados válidos: `available`, `occupied`, `reserved`, `in_cleaning`.

- Body (JSON):

```json
{
  "status": "reserved"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "status": "reserved",
  "tableNumber": 10
}
```

---

## Órdenes

### 44) Crear orden

- Método y ruta: `POST /api/orders/`

- Descripción: Crea una nueva orden asociada a una mesa.

- Body (JSON):

```json
{
  "tableId": 1,
  "waiterId": 5,
  "status": "notCooking"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "tableId": 1,
  "waiterId": 5,
  "status": "notCooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": null,
  "billId": null
}
```

### 45) Listar todas las órdenes

- Método y ruta: `GET /api/orders/`

- Descripción: Obtiene todas las órdenes del sistema.

- Respuesta 200 (JSON):

```json
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
```

### 46) Obtener una orden específica

- Método y ruta: `GET /api/orders/{id}/`

- Descripción: Obtiene los detalles de una orden específica.

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "tableId": 1,
  "waiterId": 5,
  "status": "notCooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": null,
  "billId": null
}
```

### 47) Actualizar orden

- Método y ruta: `PUT /api/orders/{id}/`

- Descripción: Actualiza los datos de una orden (actualización parcial permitida).

- Body (JSON):

```json
{
  "status": "cooking",
  "waiterId": 3
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "tableId": 1,
  "waiterId": 3,
  "status": "cooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": "2025-11-13T20:10:00Z",
  "billId": null
}
```

### 48) Actualizar estado de una orden

- Método y ruta: `PUT /api/orders/{id}/update_status/`

- Descripción: Cambia el estado de una orden. Estados válidos: `notCooking`, `cooking`, `ready`.

- Body (JSON):

```json
{
  "status": "cooking"
}
```

- Respuesta 200 (JSON):

```json
{
  "id": 1,
  "tableId": 1,
  "waiterId": 5,
  "status": "cooking",
  "createdAt": "2025-11-13T20:00:00Z",
  "updatedAt": "2025-11-13T20:10:00Z",
  "billId": null
}
```

### 49) Obtener items de una orden

- Método y ruta: `GET /api/orders/{id}/get_items/`

- Descripción: Lista todos los items (productos) de una orden específica.

- Respuesta 200 (JSON):

```json
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
```

### 50) Agregar item a una orden

- Método y ruta: `POST /api/orders/{id}/add_item/`

- Descripción: Agrega un producto (item) a una orden existente.

- Body (JSON):

```json
{
  "productId": 1,
  "quantity": 2,
  "note": "Sin cebolla"
}
```

- Respuesta 201 (JSON):

```json
{
  "id": 1,
  "orderId": 1,
  "productId": 1,
  "quantity": 2,
  "note": "Sin cebolla"
}
```

### 51) Eliminar orden

- Método y ruta: `DELETE /api/orders/{id}/`

- Descripción: Elimina una orden del sistema.

- Respuesta 204 (sin contenido)

---

## Facturación (Bills)

### 52) Crear factura para una mesa

- Método y ruta: `POST /bills/create_bill/{table_id}/`

- Descripción: Crea una factura agrupando todas las órdenes de la mesa que no tienen factura. Calcula automáticamente IVA (15%) y total.

- Body (JSON):

```json
{
  "cashier": "Juan Pérez",
  "paymentMethod": "cash",
  "discount": 0
}
```

- Respuesta 201 (JSON):

```json
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
```

### 53) Listar todas las facturas

- Método y ruta: `GET /bills/`

- Descripción: Obtiene todas las facturas del sistema.

- Respuesta 200 (JSON):

```json
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
```

### 54) Obtener una factura específica

- Método y ruta: `GET /bills/{id}/`

- Descripción: Obtiene los detalles de una factura específica.

- Respuesta 200 (JSON):

```json
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
```

### 55) Listar facturas no pagadas

- Método y ruta: `GET /bills/get_not_payed_bills/`

- Descripción: Lista todas las facturas con estado "notPayed".

- Respuesta 200 (JSON):

```json
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
```

### 56) Listar facturas pagadas

- Método y ruta: `GET /bills/get_payed_bills/`

- Descripción: Lista todas las facturas con estado "payed".

- Respuesta 200 (JSON):

```json
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
```

### 57) Actualizar valores de una factura

- Método y ruta: `PUT /bills/{id}/update_bill/`

- Descripción: Actualiza IVA y descuento de una factura. Solo se puede modificar si no está pagada.

- Body (JSON):

```json
{
  "IVA": 15,
  "discount": 50
}
```

- Respuesta 200 (JSON):

```json
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
```

### 58) Actualizar estado de una factura

- Método y ruta: `PUT /bills/{id}/update_status/`

- Descripción: Cambia el estado de pago de una factura. Estados válidos: `notPayed`, `payed`.

- Body (JSON):

```json
{
  "status": "payed"
}
```

- Respuesta 200 (JSON):

```json
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
```

### 59) Eliminar factura

- Método y ruta: `DELETE /bills/{id}/`

- Descripción: Elimina una factura del sistema.

- Respuesta 204 (sin contenido)

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

# Backend Refactoring Guide

## Overview

This document outlines the refactoring completed to align all `views.py` files with the new model structure documented in `docs/`.

## Problem Statement

The backend models were refactored to follow a better structure (separating order headers from order items, adding proper relationships), but all `views.py` files became outdated and incompatible with the new models.

## New Model Structure

### Tables App

**table**
- `id`: AutoField (primary key)
- `status`: CharField (available, occupied, reserved, in_cleaning)
- `tableNumber`: IntegerField

**order** (Order Header)
- `id`: AutoField (primary key)
- `status`: CharField (notCooking, cooking, ready)
- `tableId`: ForeignKey to table
- `billId`: ForeignKey to bill (nullable - orders created before billing)
- `createdAt`: DateTimeField (auto)
- `updatedAt`: DateTimeField (nullable)
- `waiterId`: IntegerField

**orderItem** (Order Line Items)
- `id`: AutoField (primary key)
- `orderId`: ForeignKey to order
- `productId`: ForeignKey to product
- `quantity`: IntegerField
- `note`: TextField (optional)

### Menu App

**productCategory**
- `id`: AutoField (primary key)
- `name`: CharField

**product**
- `id`: AutoField (primary key)
- `name`: CharField
- `price`: IntegerField
- `categoryId`: ForeignKey to productCategory (nullable)

### Bill App

**bill**
- `id`: AutoField (primary key)
- `status`: CharField (notPayed, payed)
- `tableId`: ForeignKey to table
- `createdAt`: DateTimeField (auto)
- `closedAt`: DateTimeField (nullable)
- `paidAmount`: FloatField (default: 0)
- `paymentMethod`: CharField (optional)
- `cashier`: CharField (optional)
- `IVA`: IntegerField (optional, default: 0)
- `discount`: FloatField (optional, default: 0)
- `total`: FloatField (default: 0)

## Changes Made

### 1. tables/views.py

**Problem**: Views tried to create flat order objects with `product`, `quantity`, `note` fields that don't exist in the new model.

**Solution**:
- Updated `add_order` action to create an order header first
- Then create orderItem instances for each product
- Added `OrderItemLegacySerializer` to maintain backward-compatible API responses
- The API still accepts `[{"product": id, "quantity": num, "note": "..."}]`
- But internally creates order + orderItems

### 2. tables/serializers.py

**Added**:
- `OrderItemLegacySerializer`: Converts new orderItem model to legacy flat format
- Auto-generates `tableNumber` if not provided in table creation
- Handles default values for optional fields

### 3. menu/views.py

**Problem**: 
- Had duplicate ViewSets (ProductViewSet and ProductAdminViewSet)
- Didn't handle required `categoryId` field

**Solution**:
- Merged into single `ProductViewSet` with proper create/update methods
- Auto-creates default category if not provided
- Added `ProductCategoryViewSet` for category management
- Simplified code by using ModelViewSet defaults

### 4. bill/views.py

**Problem**: Referenced `order.quantity` and `order.product` which don't exist in new model.

**Solution**:
- Updated `createBill` to iterate through orders and their orderItems
- Properly calculates totals from orderItem quantities and product prices
- Associates orders with bill via `billId` field
- Generates PDF with correct data structure

### 5. users/views.py

**Problems**:
- Missing `self` parameter in methods
- Used `get_object_or_404` on Token instead of `get_or_create`
- Typos: `serializer.erros`, `serializer.save` (missing parentheses)
- Methods weren't proper ViewSet actions

**Solution**:
- Fixed all syntax errors
- Made `login` an `@action` endpoint
- Made `register` the standard `create` method
- Added missing `Permission` import
- Fixed string formatting in responses

### 6. Model Updates

To support the new views, minimal model changes were needed:

**tables/models.py**:
- `order.billId`: Added `null=True, blank=True` (orders created before billing)
- `orderItem.note`: Added `blank=True, default=''` (notes optional)

**menu/models.py**:
- `product.categoryId`: Added `null=True, blank=True` (category optional)

**bill/models.py**:
- `paymentMethod`: Added `blank=True, default=''`
- `cashier`: Added `blank=True, default=''`
- Added defaults for IVA, discount, total

## API Compatibility

The refactoring maintains backward compatibility with the documented API in `docs/API/FrontendEndpoints.md`:

### Example: Creating Orders

**Request** (unchanged):
```json
POST /tables/{table_id}/add_order/
[
  {"product": 1, "quantity": 2},
  {"product": 2, "quantity": 1, "note": "Sin cebolla"}
]
```

**Response** (unchanged format, new internal structure):
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

Internally, this now creates:
1. One `order` object (header)
2. Two `orderItem` objects (line items)

## Migration Required

The model changes require database migration:

```bash
docker exec -it drf_backend python manage.py makemigrations
docker exec -it drf_backend python manage.py migrate
```

## Testing

To test the refactored endpoints:

```bash
# Start the services
docker compose up -d

# Run the test suite
cd backend/tests
python test_endpoints.py
```

## Future Work

### Remaining Empty Views

**inventory/views.py** and **cashRegister/views.py** are currently empty. These should be implemented based on:
- inventory/models.py structure
- cashRegister/models.py structure
- Business requirements

### Potential Improvements

1. **Add proper permissions**: Currently commented out, should be enabled
2. **Add pagination**: Large lists should be paginated
3. **Add filtering**: Allow filtering by date, status, etc.
4. **Add validation**: More robust input validation
5. **Error handling**: Better error messages and logging
6. **Tests**: Add unit tests for each endpoint

## Conventions

Following `docs/general/conventions.md`:

- Use descriptive commit messages: `refactor(tables): update views for new model structure`
- Branch naming: `feature/`, `bugfix/`, `refactor/`
- Keep PRs focused and small
- Run migrations before pushing

## Troubleshooting

### Common Issues

1. **"Field does not exist" errors**: Check model has the field, run migrations
2. **Foreign key errors**: Ensure related objects exist before creating references
3. **Validation errors**: Check serializer includes all required fields
4. **Import errors**: Verify circular imports are avoided with string references ('app.Model')

### Debug Tips

1. Check Django shell to test queries:
```python
docker exec -it drf_backend python manage.py shell
>>> from tables.models import order, orderItem
>>> order.objects.all()
```

2. Check migrations status:
```bash
docker exec -it drf_backend python manage.py showmigrations
```

3. View SQL being generated:
```python
>>> queryset = order.objects.filter(tableId=1)
>>> print(queryset.query)
```

## Summary

All `views.py` files have been successfully updated to work with the refactored models while maintaining backward compatibility with the documented API. The changes are minimal, focused, and preserve existing functionality.

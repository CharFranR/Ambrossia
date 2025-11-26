from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import inventorySupplyViewSet, InventorySupplyTypeViewSet, InventoryMovementTypeViewSet

router = DefaultRouter()
router.register(r'InventorySupply', inventorySupplyViewSet, basename = 'InventorySupply')
router.register(r'InventorySupplyType', InventorySupplyTypeViewSet, basename='InventorySupplyType')
router.register(r'InventoryMovementType', InventoryMovementTypeViewSet, basename='InventoryMovementType')

URLPattern = [
    path('', include(router.urls)),
    path('',include(router.urls)),
    path('',include(router.urls))
]
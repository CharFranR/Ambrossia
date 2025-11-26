from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import inventorySupplyViewSet, InventorySupplyTypeViewSet, InventoryMovementTypeViewSet

router = DefaultRouter()
router.register(r'inventorysupply', inventorySupplyViewSet, basename = 'inventorysupply')
router.register(r'inventorySupplyType', InventorySupplyTypeViewSet, basename='InventorySupplyType')
router.register(r'inventoryMovementType', InventoryMovementTypeViewSet, basename='InventoryMovementType')

urlpatterns = [
    path('', include(router.urls)),
]
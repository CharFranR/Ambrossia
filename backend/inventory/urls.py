from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import InventoryProductViewSet, InventoryProductTypeViewSet, InventoryMovementTypeViewSet

router = DefaultRouter()
router.register(r'InventoryProduct', InventoryProductViewSet, basename = 'InventoryProduct')
router.register(r'InventoryProductType', InventoryProductTypeViewSet, basename='InventoryProductType')
router.register(r'InventoryMovement', InventoryMovementTypeViewSet, basename='InventoryMovementT')

URLPattern = [
    path('', include(router.urls)),
    path('',include(router.urls)),
    path('',include(router.urls)),
    path('',include(router.urls))
]
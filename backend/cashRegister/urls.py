from rest_framework.routers import DefaultRouter
from .views import CashRegisterViewSet, cashMovementViewSet, billsQuantitySerilizerViewSet

router = DefaultRouter()
router.register(r'cashRegister', CashRegisterViewSet, basename='cashRegister')
router.register(r'cashMovement', cashMovementViewSet, basename= "cashMovement")
router.register(r'billsQuantity', billsQuantitySerilizerViewSet, basename="billsQuantity")

urlpatterns = router.urls
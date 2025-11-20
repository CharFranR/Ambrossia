from rest_framework.routers import DefaultRouter
from .views import CashRegisterViewSet, CashMovementViewSet, BillsQuantityViewSet

router = DefaultRouter()
router.register(r'cashRegister', CashRegisterViewSet, basename='cashRegister')
router.register(r'cashMovement', CashMovementViewSet, basename= "cashMovement")
router.register(r'billsQuantity', BillsQuantityViewSet, basename="billsQuantity")

urlpatterns = router.urls
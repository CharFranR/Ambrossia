from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category', ProductCategoryViewSet, basename='category')

urlpatterns = router.urls
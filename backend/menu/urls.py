
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet, CookbookViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'productCategory', ProductCategoryViewSet, basename='productCategory')
router.register(r'cookbook', CookbookViewSet, basename='cookbook')

urlpatterns = router.urls
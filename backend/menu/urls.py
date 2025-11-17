
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet, CookbookViewSet, IngredientViewSet, CookbookIngredientViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'productCategory', ProductCategoryViewSet, basename='productCategory')
router.register(r'Cookbook', CookbookViewSet, basename='Cookbook')
router.register(r'Ingredient', IngredientViewSet, basename='Ingredient')
router.register(r'CookbookIngredient', CookbookIngredientViewSet, basename='CookbookIngredient')

urlpatterns = router.urls
from rest_framework.routers import DefaultRouter
from .views import userViewSet

router = DefaultRouter()
router.register(r'users', userViewSet, basename='users')

urlpatterns = router.urls
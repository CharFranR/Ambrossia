from rest_framework.routers import DefaultRouter
from .views import tablesViewSet

router = DefaultRouter()
router.register(r'tables', tablesViewSet, basename='tables')

urlpatterns = router.urls
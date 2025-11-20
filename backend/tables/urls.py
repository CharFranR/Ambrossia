from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import OrderViewSet, TableViewSet

router = DefaultRouter()
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router.urls)),
]
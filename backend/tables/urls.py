from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TableViewSet

router = DefaultRouter()
router.register(r'tables', TableViewSet, basename='table')

urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
    # Estas son otras rutas que podrias poner, si decides que estan separadas del ViewSet
    # path("tables/not-payed-bills/", getNotPayedBills, name="not-payed-bills"),
    # path("tables/stats/", customStats, name="table-stats"),
]
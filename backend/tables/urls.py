from django.urls import path
from .views import getStatusPerTable, addTable, getAllStatus, updateStatusPerTable

urlpatterns = [
    path('getStatusPerTable/<int:id>/', getStatusPerTable, name = "getTableStatus"),
    path('getAllStatus', getAllStatus, name = "getAllSatus"),
    path('addTable/', addTable, name = "addNewTable"),
    path('updateStatusPerTable/', updateStatusPerTable, name = "updateStatusPerTable"),
]
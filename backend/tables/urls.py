from django.urls import path
from .views import (
    getStatusPerTable, addTable, updateStatusPerTable,
    addOrder, createBill, updateBillStatus,
    getNotPayedBills, getPayedBills
)

urlpatterns = [
    path('getStatusPerTable/<int:id>/', getStatusPerTable, name="getTableStatus"),
    path('addTable/', addTable, name="addNewTable"),
    path('updateStatusPerTable/<int:id>/', updateStatusPerTable, name="updateStatusPerTable"),
    path('<int:id>/orders/', addOrder, name="addOrder"),
    path('<int:table_id>/createBill/', createBill, name="createBill"),
    path('bills/<int:bill_id>/status/', updateBillStatus, name="updateBillStatus"),
    path('getNotPayedBills/', getNotPayedBills, name="getNotPayedBills"),
    path('getPayedBills/', getPayedBills, name="getPayedBills"),
]
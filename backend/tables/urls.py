from django.urls import path
from .views import (
    getStatusPerTable, addTable, updateStatusPerTable,
    addOrder, createBill, updateBillStatus,
    getNotPayedBills, getPayedBills
)

urlpatterns = [
    # Endpoints anteriores (por si las moscas, quien sabe):
    # path('getStatusPerTable/<int:id>/', getStatusPerTable, name="getTableStatus"),
    # path('addTable/', addTable, name="addNewTable"),
    # path('updateStatusPerTable/<int:id>/', updateStatusPerTable, name="updateStatusPerTable"),
    # path('<int:id>/orders/', addOrder, name="addOrder"),
    # path('<int:table_id>/createBill/', createBill, name="createBill"),
    # path('bills/<int:bill_id>/status/', updateBillStatus, name="updateBillStatus"),
    # path('getNotPayedBills/', getNotPayedBills, name="getNotPayedBills"),
    # path('getPayedBills/', getPayedBills, name="getPayedBills"),

    path('tables/', addTable, name="table-list-create"),                              # POST
    path('tables/<int:id>/', getStatusPerTable, name="table-detail"),                 # GET
    path('tables/<int:id>/', updateStatusPerTable, name="table-update"),              # PUT
    path('tables/<int:id>/orders/', addOrder, name="order-create"),                   # POST 
    path('tables/<int:table_id>/bills/', createBill, name="bill-create"),             # POST
    path('bills/not-payed/', getNotPayedBills, name="bill-not-payed-list"),           # GET
    path('bills/payed/', getPayedBills, name="bill-payed-list"),                      # GET
    path('bills/<int:bill_id>/status/', updateBillStatus, name="bill-status-update"), # PUT
]
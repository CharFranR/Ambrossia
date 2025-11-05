from django.urls import path
from .views import (
    createBill, updateBillStatus,
    getNotPayedBills, getPayedBills,
    updateBill
)

urlpatterns = [
    path('bills/not-payed/', getNotPayedBills, name="bill-not-payed-list"),           # GET
    path('bills/payed/', getPayedBills, name="bill-payed-list"),                      # GET
    path('bills/<int:bill_id>/status/', updateBillStatus, name="bill-status-update"), # PUT
    path('tables/<int:table_id>/bills/', createBill, name="bill-create"),             # POST
    path('bills/<bill_id>', updateBill, name="bill update")                           # PUt
]
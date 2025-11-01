from django.urls import path
from .views import addProduct, getAllProducts, updateProduct

urlpatterns = [
    path("addProduct/", addProduct, name="addProduct"),
    path("getAllProducts/", getAllProducts, name="getAllProducts"),
    path("updateProduct/<int:id>/", updateProduct, name="updateProduct"),
]
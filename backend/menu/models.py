from django.db import models

# Categorias de productos
class ProductCategory(models.Model):
    name = models.CharField(max_length = 20)

# Modelos
class CookBook(models.Model):
    name = models.CharField(max_length = 200)
    note = models.TextField(blank=True)

class Product(models.Model):
    name = models.CharField(max_length = 200)
    price =  models.IntegerField()
    cookbookId = models.ForeignKey(CookBook, on_delete= models.CASCADE)
    categoryId = models.ForeignKey(ProductCategory, on_delete= models.CASCADE)

class InventoryProduct(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    lastUpdated = models.DateTimeField(auto_now=True)


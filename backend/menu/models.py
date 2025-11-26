from django.db import models

# Categorias de productos
class ProductCategory(models.Model):
    name = models.CharField(max_length = 20)

# Modelos
class CookBook(models.Model):
    name = models.CharField(max_length = 200)
    note = models.TextField(blank=True)
    preparation_time = models.IntegerField(help_text="Tiempo en minutos", null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    instructions = models.TextField(blank=True, help_text="Pasos detallados de la receta")
    is_active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)
    image = models.ImageField(upload_to='cookbook_images/', null=True, blank=True)

class Product(models.Model):
    name = models.CharField(max_length = 200)
    price =  models.IntegerField()
    cookbookId = models.ForeignKey(CookBook, on_delete= models.CASCADE)
    categoryId = models.ForeignKey(ProductCategory, on_delete= models.CASCADE)

class InventoryProduct(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    lastUpdated = models.DateTimeField(auto_now=True)


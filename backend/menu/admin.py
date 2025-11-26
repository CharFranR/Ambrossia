from django.contrib import admin
from .models import Product, ProductCategory, CookBook, InventoryProduct

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category_name", "cookbook_name")
    search_fields = ("name",)
    list_filter = ("categoryId", "cookbookId")

    def category_name(self, obj):
        return obj.categoryId.name
    category_name.short_description = 'Category'

    def cookbook_name(self, obj):
        return obj.cookbookId.name
    cookbook_name.short_description = 'Cookbook'

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

class CookBookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "note")
    search_fields = ("name",)

class InventoryProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "quantity", "lastUpdated")
    list_filter = ("lastUpdated",)
    
    def product_name(self, obj):
        return obj.productId.name
    product_name.short_description = 'Product'

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(CookBook, CookBookAdmin)
admin.site.register(InventoryProduct, InventoryProductAdmin)
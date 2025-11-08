from django.contrib import admin
from .models import product

# Register your models here.
@admin.register(product)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)
    
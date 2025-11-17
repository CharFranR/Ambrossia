from django.db import models

class productCategory(models.Model):
    name = models.CharField(max_length = 20)

class product(models.Model):
    name = models.CharField(max_length = 200)
    price =  models.IntegerField()
    categoryId = models.ForeignKey(productCategory, on_delete= models.CASCADE)

class cookbook(models.Model):
    name = models.CharField(max_length = 200)
    note = models.TextField(blank=True)

class ingredient(models.Model):
    name = models.CharField(max_length = 200)
    unit = models.CharField(max_length = 200)

class cookbookIngredient (models.Model):
    recipe = models.ForeignKey(cookbook, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(ingredient, on_delete=models.CASCADE)
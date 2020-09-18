from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class FoodUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=5)
    age = models.IntegerField()
    Repmaterial = models.CharField(max_length=100)
    pretag = models.CharField(max_length=100)

class MainFood(models.Model):
    idx = models.IntegerField()
    name = models.CharField(max_length=50, null=True)
    recipe = models.CharField(max_length=500, null=True)
    material = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=100, null=True)
 
class NutrientFood(models.Model):
    idx = models.IntegerField()
    name = models.CharField(max_length=50, null=True)
    calorie = models.FloatField(null=True)
    carbohydrate = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    Lipid = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    cholesterol = models.FloatField(null=True)
    Dietary_Fiber = models.FloatField(null=True)
    calcium = models.FloatField(null=True)
    Vitaminc = models.FloatField(null=True)
    sugars = models.FloatField(null=True)

class MyRefrigerator(models.Model):
    refrigerator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refrigerator')
    material = models.CharField(max_length=20, null=True)
    food_time = models.DateTimeField(default=timezone.now)
    shelf_life = models.IntegerField()

class GeneralFood(models.Model):
    idx = models.IntegerField()
    name = models.CharField(max_length=50, null=True)
    material = models.CharField(max_length=200, null=True)
    recipe = models.CharField(max_length=500, null=True)
    tag = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    calorie = models.FloatField(null=True)
    carbohydrate = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    Lipid = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    cholesterol = models.FloatField(null=True)
    Dietary_Fiber = models.FloatField(null=True)
    calcium = models.FloatField(null=True)
    Vitaminc = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
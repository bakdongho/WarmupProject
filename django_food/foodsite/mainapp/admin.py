from django.contrib import admin
from .models import FoodUser, MainFood, NutrientFood

# Register your models here.
admin.site.register(FoodUser)
admin.site.register(MainFood)
admin.site.register(NutrientFood)
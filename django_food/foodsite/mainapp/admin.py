from django.contrib import admin
from .models import FoodUser, MainFood, NutrientFood, MyRefrigerator, GeneralFood

# Register your models here.
admin.site.register(FoodUser)
admin.site.register(MainFood)
admin.site.register(NutrientFood)
admin.site.register(MyRefrigerator)
admin.site.register(GeneralFood)
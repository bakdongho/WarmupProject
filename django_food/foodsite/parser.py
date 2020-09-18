import csv

f1 = open('data/maindata.csv', 'r', encoding='UTF8')
f2 = open('data/nutrientdata.csv', 'r', encoding='UTF8')
f3 = open('data/general_data.csv', 'r', encoding='UTF8')

reader1 = csv.DictReader(f1)
reader2 = csv.DictReader(f2)
reader3 = csv.DictReader(f3)
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodsite.settings")
import django
django.setup()

from mainapp.models import MainFood, NutrientFood, GeneralFood

# if __name__=='__main__':
#     for row in reader1:
#         MainFood(idx=row['index'], name=row['요리이름'], recipe=row['조리법'], material=row['재료'], tag=row['태그']).save()
#         print(row['요리이름'] + 'is saved!')

# if __name__=='__main__':
#     for row in reader2:
#         NutrientFood(idx=row['index'], name=row['요리이름'], calorie=row['칼로리'], carbohydrate=row['탄수화물'], protein=row['단백질'], Lipid=row['지질'], salt=row['나트륨'], cholesterol=row['콜레스테롤'], Dietary_Fiber=row['식이섬유'], calcium=row['칼슘'], Vitaminc=row['비타민c'], sugars=row['당류']).save()
#         print(row['요리이름'] + 'is saved!')

if __name__=='__main__':
    for row in reader3:
        GeneralFood(idx=row['index'], name=row['요리이름'], recipe=row['조리법'], material=row['재료'], tag=row['태그'], category=row['카테고리'], calorie=row['칼로리'], carbohydrate=row['탄수화물'], protein=row['단백질'], Lipid=row['지질'], salt=row['나트륨'], cholesterol=row['콜레스테롤'], Dietary_Fiber=row['식이섬유'], calcium=row['칼슘'], Vitaminc=row['비타민c'], sugars=row['당류']).save()
        print(row['요리이름'] + 'is saved!')
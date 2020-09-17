from django.shortcuts import render, redirect
from .models import FoodUser, MainFood, NutrientFood
from django.contrib.auth.models import User
from django.contrib import auth
import pandas as pd

# Create your views here.
ERROR_MSG = {
    'ID_EXIST': '이미 사용 중인 아이디 입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디 입니다',
    'ID_PW_MISSING': '아이디와 비밀번호를 다시 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.',
}

def signup(request):

    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }
    if request.method == 'POST':
        
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']
        # add
        user_name = request.POST['name']
        user_gender = request.POST['gender']
        user_age = request.POST['age']
        user_repmaterial = request.POST['repmaterial']
        user_pretag = request.POST['pretag']

        if (user_id and user_pw):

            user = User.objects.filter(username=user_id)

            if len(user) == 0:

                if (user_pw == user_pw_check):

                    created_user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )
                    # add
                    FoodUser.objects.create(
                        user = created_user,
                        name = user_name,
                        gender = user_gender,
                        age = user_age,
                        Repmaterial = user_repmaterial,
                        pretag = user_pretag
                    )

                    auth.login(request, created_user)
                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html', context)

def login(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }

    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:
                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )

                if user != None:
                    auth.login(request, user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'login.html', context)
    

def logout(request):
    if request.method == 'POST':
        auth.logout(request)

    return redirect('home')

def home(request):

    return render(request, 'home.html')

def nut_result(request,category):
    dic={
        1:'당뇨',
        2:'골다공증',
        3:'고혈압',
        4:'갱년기',
        5:'감기',
        6:'비염',
    }
    nutri_obj=NutrientFood.objects.all().values()
    df=pd.DataFrame(nutri_obj)
    if category == 1:
        dig = dic[1] +'설명~~~'
    elif category == 2:
        dig = dic[2]+'설명~~~'
    elif category == 3:
        dig = dic[3]+'설명~~~'
    elif category == 4:
        dig = dic[4]+'설명~~~'
    elif category == 5:
        dig = dic[5]+'설명~~~'
    elif category == 6:
        dig = dic[6]+'설명~~~'
    filter_df = df.loc[1:5,:]
    print(filter_df)
    filter_nutri_obj=[]
    for i in filter_df.idx:
        filter_nutri_obj.append(NutrientFood.objects.get(idx=i))
    print(filter_nutri_obj)
    context = {
        'nutri': filter_nutri_obj,
        'contents' : str(dig)
    }
    
    return render(request, 'nut_result.html',context)

def nutrition(request):
    
    return render(request, 'nutrition.html')

def recipe(request):

    return render(request, 'recipe.html')

def personal(request):

    return render(request, 'personal.html')

def detail(request,food_idx):
    Main_Food=MainFood.objects.get(idx=food_idx)

    return render(request, 'detail.html',{'main_food' : Main_Food})
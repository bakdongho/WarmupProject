from django.shortcuts import render, redirect
from .models import FoodUser, MainFood, NutrientFood, MyRefrigerator
from django.contrib.auth.models import User
from django.contrib import auth
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def mypage(request, user_pk):
    Users = User.objects.get(pk=user_pk)
    Food_User = FoodUser.objects.get(user=Users)
    MyRefrigerator_User = MyRefrigerator.objects.filter(refrigerator=Users)

    context = {

        'user': Users,
        'food_user': Food_User,
        'refrigerator_user': MyRefrigerator_User
    }
    
    return render(request, 'mypage.html', context)

def edit_refrigerator(request, user_pk, refrigerator_pk):
    Users = User.objects.get(pk=user_pk)
    Refrigerator_User = MyRefrigerator.objects.get(refrigerator=Users, pk=refrigerator_pk)
    
    if request.method == 'POST':
        update_refrigerator = MyRefrigerator.objects.filter(refrigerator=Users, pk=refrigerator_pk)

        update_refrigerator.update(
            material = request.POST['material'],
            shelf_life = request.POST['shelf_life']
        )

        return redirect('/mypage/' + str(user_pk))
    
    context = {
        'user': Users,
        'refrigerator_user': Refrigerator_User,
    }

    return render(request, 'edit_refrigerator.html', context)

def delete_refrigerator(request, user_pk, refrigerator_pk):
    Users = User.objects.get(pk=user_pk)
    target_refrigerator = MyRefrigerator.objects.get(refrigerator=Users, pk=refrigerator_pk)
    target_refrigerator.delete()

    return redirect('/mypage/' + str(user_pk))

def edit_user(request, user_pk):
    Users = User.objects.get(pk=user_pk)
    Food_User = FoodUser.objects.get(user=Users)

    if request.method == 'POST':
        update_fooduser = FoodUser.objects.filter(pk=Food_User.pk)

        update_fooduser.update(
            name = request.POST['name'],
            gender = request.POST['gender'],
            age = request.POST['age'],
            Repmaterial = request.POST['repmaterial'],
            pretag = request.POST['pretag'],
        )

        return redirect('/mypage/' + str(user_pk))

    context = {
        'user': Users,
        'fooduser': Food_User
    }
    return render(request, 'edit_user.html', context)

def add_refrigerator(request, user_pk):
    Users = User.objects.get(pk=user_pk)

    if request.method == 'POST':
        # add_refrigerator_user = MyRefrigerator.objects.filter(pk=refrigerator_User.pk)
        
        materials = request.POST['material']
        shelf_lifes = request.POST['shelf_life']

        MyRefrigerator.objects.create(
            refrigerator = Users,
            material = materials,
            shelf_life = shelf_lifes,
        )
        return redirect('/mypage/' + str(user_pk))

    return render(request, 'add_refrigerator.html')

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

def personal(request, user_pk):
    Users = User.objects.get(pk=user_pk)
    MyRefrigerator_User = MyRefrigerator.objects.filter(refrigerator=Users).values()
    Food_User = FoodUser.objects.get(user=Users)

    # 전처리
    datas = pd.DataFrame(MyRefrigerator_User)
    datas = datas.sort_values(by='shelf_life', ascending=True)
    datas = datas.drop(['refrigerator_id'], axis='columns')
    # print(datas) 
    
    # user 기피재료, 선호태그
    hate_food = Food_User.Repmaterial.split(' ')
    like_tag = Food_User.pretag.split(' ')
    # print(hate_food[1])

    # 기피재료 빼기
    sw_materials = []    # 미역, 김
    for i in datas['material']:
        for j in hate_food:
            if i == j:
                sw_materials.append(i)
    # print(sw_material)

    for i in sw_materials:
        drop_index = datas[datas['material'] == i].index
        datas = datas.drop(drop_index)
    # print(datas)
    
    # 유통기한 자르기
    count = 0
    use_materials = datas[0:3]
    # print(use_materials)
    add_material = 2    # 더할 재료개수 (0일경우 기본 3개)
    deadline = 7    # 유통기한 마감날짜 

    for i in range(len(datas[3:])):
        if count != add_material:  
            if datas[3+i:4+i].shelf_life.item() <= deadline:
                use_materials = use_materials.append(datas[3+i:4+i])
                count += 1
    # print(use_materials)

    user_materials = ''
    for i in use_materials['material']:
        user_materials = user_materials + i + ' '
    print('사용재료: ', user_materials)


    # content 유사도 구하기
    data = MainFood.objects.all().values()
    df = pd.DataFrame(data)

    # 냉장고 재료 데이터 넣기
    user_data = {'idx':5220, 'name':'user', 'recipe':' ', 'material':user_materials, 'tag':' '}
    df = df.append(user_data, ignore_index=True)

    # TFIDF
    # tfidf_vec = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_vec = TfidfVectorizer()
    tfidf_matrix = tfidf_vec.fit_transform(df['material'])
    # print(tfidf_vec.vocabulary_.items())
    # print(tfidf_matrix.shape)


    # 유사도
    genres_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # print(genres_similarity)
    similar_index = np.argsort(-genres_similarity)
    # print(similar_index)

    # 냉장고 재료와 비슷한 것 뽑기
    user_index = df[df['name']=='user'].index.values

    similar_food = similar_index[user_index, 1:6]
    similar_food_index = similar_food.reshape(-1)
    data = df.iloc[similar_food_index]
    # print(data)

    print('========================================= 유사도 측정 결과 >> 요리 List =====================================================')
    print(df.iloc[similar_food_index]['name'])

    food_idx = []
    for i in df.iloc[similar_food_index]['idx']:
        food_idx.append(i)
    print(food_idx)


    context = {
        'user': Users,
        'use_materials': use_materials,
        'data': data,
        'food_idx1': food_idx[0],
        'food_idx2': food_idx[1],
        'food_idx3': food_idx[2],
        'food_idx4': food_idx[3],
        'food_idx5': food_idx[4],
    }
    return render(request, 'personal.html', context)

def detail(request,food_idx):
    Main_Food = MainFood.objects.get(idx=food_idx)


    return render(request, 'detail.html',{'main_food' : Main_Food})
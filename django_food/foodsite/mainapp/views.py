from django.shortcuts import render, redirect
from .models import FoodUser, MainFood, NutrientFood, MyRefrigerator, GeneralFood
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
        1:['감기','설명~~'],
        2:['비만','설명~~'],
        3:['빈혈','설명~~'],
        4:['고혈압','설명~~'],
        5:['심부전','설명~~'],
        6:['고지혈증','설명~~'],
        7:['당뇨','설명~~'],
        8:['심근경색','설명~~'],
        9:['뇌졸중','설명~~'],
        10:['골다공증','설명~~']
    }
    GeneralFood_obj=GeneralFood.objects.all().values()
    df=pd.DataFrame(GeneralFood_obj)

    if category == 1:
    # 감기
        df = df[df['material'].str.contains('우유|초콜렛|초콜릿|사과|라임')==False]
        df = df[df['material'].str.contains('콩나물|더덕|모과|무|배|도라지|칡|생강|유자|호박|대추|오렌지|포도|레몬|녹차|꿀|딸기|귤|피망|고추|브로콜리|굴')]
        df = df[df['name'].str.contains('차|스프|죽|미음')]
        filter_df = df.sort_values(by=['Vitaminc', 'protein'], ascending=[False, False])
    elif category == 2:
    # 비만
        df = df[df['tag'].str.contains('다이어트')]
        df = df[df['material'].str.contains('설탕|버터|마가린|쇠고기|소고기|돼지고기|스팸|흰밥|빵|떡')==False]
        df = df[df['material'].str.contains('다시마|미역|닭가슴살|아보카도|생강|대추|콩|자몽')]
        df = df[df['name'].str.contains('과자|쿠키|빵|떡')==False]
        filter_df = df.sort_values(by=['carbohydrate','salt','sugars'], ascending=[True, True, True])
    elif category == 3:
    # 빈혈
        df = df[df['tag'].str.contains('빈혈')]
        df = df[df['material'].str.contains('밀가루|녹차|커피|초콜릿|초콜렛')==False]
        df = df[df['material'].str.contains('시금치|땅콩|소고기|쇠고기|노른자|미역|브로콜리|레드비트|굴|토마토|체리|연어')]
        filter_df = df.sort_values(by=['Vitaminc', 'protein'], ascending=[False, False])
    elif category == 4:
    # 고혈압
        df = df[df['material'].str.contains('빵|밀가루|버터|마가린|치즈|햄|조개|마요네즈|새우|김치')==False]
        df = df[df['material'].str.contains('양파|마늘|시금치|바나나|계피|올리브오일|비트|귀리')]
        filter_df = df.sort_values(by=['calcium','Vitaminc','Dietary_Fiber'], ascending=[False, False, False])
    elif category == 5:
    # 심부전
        df = df[df['material'].str.contains('고추|겨자|카레|우엉|파|부추|고구마|밀가루')==False]
        df = df[df['material'].str.contains('두부|바나나|콩|호두|요거트')]
        df = df[df['name'].str.contains('튀김|차|도넛')==False]
        filter_df = df.sort_values(by=['cholesterol', 'Lipid', 'salt','protein', 'Dietary_Fiber'], ascending=[True, True, True, False, False])
    elif category == 6:
    # 고지혈증
        df = df[df['material'].str.contains('기름|마가린|빵|커피|베이컨|소시지|소세지|햄|치즈')==False]
        df = df[df['material'].str.contains('양파|마늘|파|토마토|호두|아몬드|카레')]
        df = df[df['name'].str.contains('라면|과자|아이스크림|빵|케이크')==False]
        filter_df = df.sort_values(by=['Vitaminc','Dietary_Fiber', 'carbohydrate','sugars','cholesterol'], ascending=[False,False, True, True, True])
    elif category == 7:
    # 당뇨
        df = df[df['material'].str.contains('설탕|밀가루|조청|치즈|흰|버터')==False]
        df = df[df['material'].str.contains('현미|시금치|콩|두부|순두부|토마토|양파|대추|표고버섯|당근|녹두|고구마|옥수수|청국장|호두|둥글레|두릅|마늘|팥')]
        df = df[df['name'].str.contains('라면|과자|아이스크림|빵|케이크|젓갈|장아찌|주스|쥬스|튀김|조림')==False]
        filter_df = df.sort_values(by=['Dietary_Fiber', 'carbohydrate','sugars'], ascending=[False, True, True])
    elif category == 8:
    # 심근경색
        df = df[df['material'].str.contains('돼지갈비|소갈비|등심|안심|삼겹살|곱창|내장|햄|소시지|베이컨|버터|마요네즈|우유|생크림|치즈|밀가루|새우|장어|미꾸라지|오징어')==False]
        df = df[df['material'].str.contains('고등어|연어|참치|동태|갈치|두부|호두|아몬드|땅콩|콩')]
        df = df[df['name'].str.contains('튀김|도넛')==False]
        filter_df = df.sort_values(by=['Dietary_Fiber','salt', 'Lipid','cholesterol'], ascending=[False, True, True, True])
    elif category == 9:
    # 뇌졸중
        df = df[df['material'].str.contains('오징어|새우|게|소시지|햄|베이컨|초콜릿|밀가루|치즈')==False]
        df = df[df['material'].str.contains('고등어|토마토|당근|사과|배|베리|아보카도|정어리|멜론|수박|녹차|귀리|생강|꽁치|부추|미역|다시마|연어|매생이')]
        filter_df = df.sort_values(by=['Dietary_Fiber','Vitaminc','salt'], ascending=[False,False, True])
    elif category == 10:
    # 골다공증
        df = df[df['material'].str.contains('설탕|소금|커피')==False]
        df = df[df['material'].str.contains('우유|요거트|요구르트|고등어|연어|표고버섯|멸치|사과|귤|콩|콩나물|순두부|두부|아몬드|냉이|고사리|김|다시마|가오리|명태')]
        filter_df = df.sort_values(by=['calcium', 'Vitaminc','salt'], ascending=[False, False, True])

    
    
    filter_food_obj=[]
    count=0
    for i in filter_df.idx:
        if count<5 : 
            filter_food_obj.append(GeneralFood.objects.get(idx=i))
            count+=1
        else:
            break
    context = {
        'nutri': filter_food_obj[:4],
        'contents' : dic[category][1],
        'title' : dic[category][0]
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
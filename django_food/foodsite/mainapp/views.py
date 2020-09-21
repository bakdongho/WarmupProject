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
        1:['감기','감기는 바이러스에 의해 코와 목 부분을 포함한 상부 호흡기계의 감염 증상으로, 사람에게 나타나는 가장 흔한 급성 질환 중 하나이다. 통계에 따르면, 전 세계적으로 매년 10억 명이 감기에 걸리는 것으로 알려져 있다. 감기에 걸렸을 때는 충분한 양의 단백질을 섭취해 몸에 근력을 보충하고, 과일에서 발견되는 비타민C를 섭취해 면역 시스템의 활동량을 증가시켜야 한다. 또한, 죽이나 스프와 같이 뜨거운 액체가 몸 속에 들어가면 체온을 유지해준다.','좋은 음식 : 파, 모과, 꿀, 박하, 대추, 생강, 도라지, 배 등등 \n 좋은 영양소 : 비타민 C, 비타민 A, 비타민 E 등등'],
        2:['비만','지방은 비만의 원인이 되는 동시에 콜레스테롤이 혈관 벽에 달라붙는 것을 촉진해 혈액순환을 막아 심장마비나 중풍을 야기한다. 따라서 혈관에 노폐물이 적게 쌓이게 하려면 지방과 콜레스테롤이 적은 음식을 먹는 것이 좋다. 설탕, 버터가 들어간 음식이나 가공식품의 섭취를 줄이고, 직접 요리할 때는 견과류, 해조류, 콩, 생강, 계피, 아보카도, 자몽 등과 같이 지방을 태우는 재료를 활용하는 것이 좋다.','좋은 음식 : 계피, 고추, 녹차, 베리류, 달걀, 견과류 등등 \n 좋은 영양소 : B 비타민류, 비타민C, 마그네슘 등등'],
        3:['빈혈','빈혈은 전 세계적으로 가장 흔히 볼 수 있는 영양결핍으로, 혈액 내 적혈구 수가 적거나 헤모글로빈양이 감소해 혈액의 산소운반 능력이 감소하는 질병을 말한다. 빈혈의 주된 증상은 피로이며, 창백한 피부, 숨이 참, 어지러움, 두통, 추위를 많이 타는 증상 등이 나타나는데, 어린아이의 경우 밥을 잘 안 먹고, 잘 보채며, 자주 칭얼거리는 모습을 보이기도 한다. 대부분의 경우 음식을 골고루 먹으면 빈혈을 예방할 수 있다.','좋은 음식 : 간, 굴, 계란 노른자, 살코기, 두부, 두유, 치즈 등등 \n 좋은 영양소 :  철분, 엽산, 비타민B12 등등'],
        4:['고혈압','고혈압은 혈압이 심각한 수준까지 올라가도 증상을 느끼지 못하는 경우가 많기 때문에 ‘침묵의 살인자’로 불린다. 고혈압은 유전적 요인과 함께 환경적 요인도 주요한 원인으로 꼽힌다. 이는 가족들이 같은 환경에서 식생활을 하기 때문에 후천적 영향으로 인한 발생률도 높다는 것이다. 고혈압을 막기 위해서는 소금(나트륨)과 포화지방이 많이 든 음식 섭취량을 줄이는 등의 노력이 필요하다. 또한 꾸준한 운동과 과일, 채소 등을 더 많이 먹는 등 식습관 개선으로 혈압을 자연스럽게 낮출 수 있다.','좋은 음식 : 양파, 마늘, 시금치, 바나나, 계피, 올리브오일 등등 \n 좋은 영양소 : 오메가3 지방산, 칼륨, 마그네슘 등등'],
        5:['심부전','심부전이란 혈액을 신체 기관에 적절히 공급해야 하는 심장의 펌프 기능에 장애가 온 상태를 말한다. 심장은 2개의 심장과 심실로 구성되어 있으며 전신에 혈액을 공급하는 중요한 역할을 한다. 그런데 심방과 심실의 수축이나 이완 기능에 문제가 생겨 심장이 혈액을 보내주는 역할을 제대로 하지 못하게 되면 이를 심부전이라 한다. 심부전이 있다면 나트륨 함량이 높은 음식을 줄이고, 살코기 위주의 단백질이 포함된 육류, 콩, 두부, 요거트 등을 섭취해야 한다.','좋은 음식 : 감자, 토마토, 시금치, 셀러리 등등 \n 좋은 영양소 : 단백질, 비타민 B군, 엽산 및 리보플라빈 등등'],
        6:['고지혈증','고지혈증이란 혈액 속에 콜레스테롤이나 중성지방 등의 지방 성분이 비정상적으로 많아지는 질환을 말한다. 총 콜레스테롤이 240mg/dL 이상이거나 중성지방이 200mg/dL 이상이면 고지혈증으로 진단한다. 기름진 식사, 잦은 음주와 흡연 등으로 고지혈증이 생기면 혈관 내에 지방침전물이 쌓여 혈관이 막히고 혈관 벽에 염증이 생기거나 두꺼워져 동맥경화, 협심증 등을 유발할 수 있다. 고지혈증에 피해야 할 음식은 육류 기름, 라면, 마가린, 과자, 아이스크림 등이다. ','좋은 음식 : 비트, 양파, 다시마, 브로콜리, 들기름 등등 \n 좋은 영양소 : 식이섬유, 오메가3, 칼륨 등등'],
        7:['당뇨','당뇨는 평소에는 신체에 심각한 증상을 보이지 않다가 잔 질병이라도 걸리면 합병증을 유발하면서 큰 병으로 만드는 무서운 병이라고 할 수 있다. 그래서 무엇보다 당뇨는 평소에 꾸준한 관리가 필요하고, 특히 식이요법이 중요하다. 일반적으로 당뇨에 좋은 음식은 칼로리가 낮고 혈당을 높게 올리지 않는 음식이다. 야채나 과일 등은 섬유질을 섭취할 수 있도록 튀기거나 볶는 조리법을 피하고, 삶거나 굽는 조리법을 사용하는 것이 좋다. 또한, 소금이 많은 음식은 혈압을 높여주기 때문에 김치, 된장, 젓갈류, 장아찌류의 섭취를 줄이는 게 좋다.','좋은 음식 : 오트밀, 통곡물 빵, 콩류, 고구마, 냉수성 어류 등등 \n 좋은 영양소 : 아연, 망간, 마그네슘, 비타민 B군, 비타민 D,E 등등'],
        8:['심근경색',"겨울에는 기온이 떨어지며 심장질환 발생률이 높아진다. 기온이 내려가면 몸의 혈관이 급격히 수축하는 탓이다. 이럴 때일수록 심장에 해로운 음식을 피해야 한다. 가장 먼저 피해야 할 음식은 튀김, 도넛 등 '트랜스 지방'이 함유된 음식이다. 가공육도 지방 부위를 많이 이용하기 때문에 콜레스테롤과 나트륨 함량이 높아 혈압을 높일 수 있으니 주의해야 한다. 심장 건강에 좋은 음식은 과일, 견과류, 생선이다. 여기에는 각종 비타민과 미네랄이 풍부하게 들어 있어서 심장 혈관을 보호하는 역할을 한다.",'좋은 음식 : 곡류, 콩류, 야채류, 과일 등등 \n 좋은 영양소 : 비타민C, 베타 카로텐, 비타민 E 등등'],
        9:['뇌졸중','암, 심장질환과 함께 3대 사망원인의 하나이며 단일 질환으로는 국내 사망률 1위를 차지하는 무서운 질병이다. 뇌졸중이란 뇌혈관이 막혀서 뇌손상을 발생시키는 ‘뇌경색’과 뇌혈관이 터져서 생기는 ‘뇌출혈’을 모두 일컫는 말로 흔히 ‘중풍’이라고 알려져 있다. 뇌경색은 뇌조직의 손상에 따른 신체·정신적 장애를 일으키는 질환이다. 뇌졸중에 좋은 음식은 등푸른 생선, 토마토, 당근, 사과, 배, 부추, 미역, 매생이 등이 있다.','좋은 음식 : 등푸른 생선, 해조류, 토마토, 사과, 배 등등 \n 좋은 영양소 : 오메가 3, 비타민 D, 마그네슘, 아연 등등'],
        10:['골다공증','골다공증은 뼈의 강도가 약해져서 골절이 일어날 가능성이 높은 상태다. 특별한 증상이 없어 모른 채로 방치하다 골절 등의 부상을 입기 쉽다. 따라서 평소에 골다공증에 좋은 음식을 알아두고 챙겨 먹는 것이 좋다. 칼슘은 뼈의 생성을 돕고 파괴를 억제한다. 우유 및 유제품, 잔멸치, 뱅어포 등에 풍부하다. 칼슘을 섭취할 때 염분이 많은 식품은 피해야 한다. 염분은 체내에서 칼슘의 흡수를 방해하기 때문이다.','좋은 음식 : 유제품, 두부, 케일, 브로콜리, 멸치 등등 \n 좋은 영양소 : 칼슘, 비타민 D,K, 식물성 단백질']
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
        'nutri': filter_food_obj,
        'description': dic[category][1],
        'contents' : dic[category][2],
        'title' : dic[category][0]
    }
    
    return render(request, 'nut_result.html',context)


def recipe(request):
    
    return render(request, 'recipe.html')

def search_result(request):
    GeneralFood_obj=GeneralFood.objects.all().values()
    df=pd.DataFrame(GeneralFood_obj)
    if request.method == 'POST':

        input_food = request.POST['input_food']
        
        df = df[df['name'].str.contains(input_food)|df['material'].str.contains(input_food)]

        search_food_obj = []
        for i in df.idx:
            search_food_obj.append(GeneralFood.objects.get(idx=i))

        context={
            'search_foodname' : input_food,
            'search_result_1' : search_food_obj[:7],
            'search_result_2' : search_food_obj[7:14],
            'search_result_3' : search_food_obj[14:21]
            }

    return render(request, 'search_result.html', context)


def category_result(request,category):
    dic={
        1:['국물 요리','키워드: 국/탕/술안주'],
        2:['면 요리','키워드: 면/비빔면/국물면'],
        3:['찜 요리','키워드: 찜/돼지고기/술안주'],
        4:['색다른 요리','키워드: 이국적인 맛/손님/접대'],
        5:['디저트','키워드: 빵/케이크/양식'],
        6:['김밥/롤/주먹밥','키워드: 김밥/롤/주먹밥'],
        7:['콩/두부 요리','키워드: 콩/두부/다이어트'],
        8:['햄/소시지 요리','키워드: 햄/소시지'],
        9:['나들이 요리','키워드: 나들이/샌드위치/양식'],
        10:['건강한 요리','키워드: 건강/예방/아이']
    }
    GeneralFood_obj=GeneralFood.objects.all().values()
    df=pd.DataFrame(GeneralFood_obj)

    if category == 1:
        df = df[df['category']=='국물 요리']
        
    elif category == 2:

        df = df[df['category']=='면 요리']

    elif category == 3:
        df = df[df['category']=='찜 요리'] 

    elif category == 4:
        df = df[df['category']=='색다른 요리']

    elif category == 5:
        df = df[df['category']=='디저트 요리']

    elif category == 6:
        df = df[df['category']=='김밥/롤/주먹밥']

    elif category == 7:
        df = df[df['category']=='콩/두부 요리']

    elif category == 8:
        df = df[df['category']=='햄/소시지 요리']

    elif category == 9:
        df = df[df['category']=='나들이 요리']

    elif category == 10:
        df = df[df['category']=='건강을 위한 요리']

    
    
    category_food_obj=[]
    for i in df.idx:
        category_food_obj.append(GeneralFood.objects.get(idx=i))
    context = {
        'in_category_1': category_food_obj[:20],
        'in_category_2': category_food_obj[20:40],
        'in_category_3': category_food_obj[40:60],
        'contents' : dic[category][1],
        'title' : dic[category][0]
    }
    
    return render(request, 'category_result.html', context)

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
    Main_Food = GeneralFood.objects.get(idx=food_idx)
    recipe_pre = Main_Food.recipe.replace("'","\n").replace("]","")
    material_pre = Main_Food.material.replace("'","")
    context={
        'recipe': recipe_pre,
        'material': material_pre,
        'main_food':Main_Food
    }

    return render(request, 'detail.html',context)
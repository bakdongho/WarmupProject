from django.shortcuts import render, redirect
from .models import FoodUser, MainFood, NutrientFood, MyRefrigerator
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
ERROR_MSG = {
    'ID_EXIST': '이미 사용 중인 아이디 입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디 입니다',
    'ID_PW_MISSING': '아이디와 비밀번호를 다시 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.',
}

def home(request):

    return render(request, 'home.html')

def nut_result(request):

    return render(request, 'nut_result.html')

def nutrition(request):

    return render(request, 'nutrition.html')

def recipe(request):

    return render(request, 'recipe.html')

def personal(request):

    return render(request, 'personal.html')

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
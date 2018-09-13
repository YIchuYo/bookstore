from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from mainsite.models import User

# Create your views here.
def login(request):
    print('1')
    print(request.body)
    if 'username' in request.POST and 'password' in request.POST:
        back = match_user_password(request.POST['username'], request.POST['password'])
        if back == 1:
            # success
            return render(request, 'login.html', {'message':'登录成功' + request.POST['username'] + request.POST['password']})
        elif back == 0:
            # no user
            return render(request, 'login.html', {'message':'用户名错误'})
        else:
            # password wrong
            return render(request, 'login.html', {'message':'密码错误'})
    else:
        return render(request, 'login.html')

def register(request):
    from mainsite.models import User

    print('username' in request.POST)
    if 'username' in request.POST and 'password' in request.POST:
        print(request.POST['username'])
        print(request.POST['password'])
        person = User()
        person.username = request.POST['username']
        person.password = request.POST['password']
        if not select_user_password(person.username):
            person.save()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'register.html')
    else:
        return render(request,'register.html')

# 用户名是否重复
def select_user_password(username_):
    return User.objects.filter(username=username_).exists()

def match_user_password(username, password):
    userset = User.objects.filter(username=username)
    if len(userset) == 1:
        for user in userset:
            if user.username == username and user.password == password:
                return 1
            elif user.username == username and user.password != password:
                return 2
    else:
        return 0


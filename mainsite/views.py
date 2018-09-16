from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainsite.models import *
from cart.cart import Cart
import os
import math

# Create your views here.
def login(request):
    if not 'username' in request.session:
        if request.method == 'POST':
            if 'username' in request.POST and 'password' in request.POST:
                back = match_user_password(request.POST['username'], request.POST['password'])
                if back == 1:
                    request.session['username'] = request.POST['username']
                    # success
                    # return render(request, 'login.html', {'message':'登录成功' + request.POST['username'] + request.POST['password']})
                    return HttpResponseRedirect(reverse('index'))
                elif back == 0:
                    # no user
                    return render(request, 'login.html', {'message':'用户名错误'})
                else:
                    # password wrong
                    return render(request, 'login.html', {'message':'密码错误'})
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')

    else:
        return render(request, 'login.html', {'message':'用户' + request.session['username'] + '已登录'})

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect(reverse('index'))

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



def index(request):

    usernow = checkUser(request)

    books = Book.objects.get_queryset().order_by('id')
    # 增加分页功能, 10本图书分为一页
    paginator = Paginator(books, 10)
    if request.method == 'GET':
        p = request.GET.get('p')
    else:
        p = '1'

    try:
        items = paginator.page(p)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    dict_book = {}
    dict_book['booklist'] = items
    dict_book['usernow'] = usernow
    for i in range(len(items)):
        items[i].image = Picture.objects.filter(bookid=items[i].id)[0].image

    return render(request, 'index.html', dict_book)


# 获取书籍信息
def bookinfo(request, id):
    usernow = checkUser(request)
    # 导入图书类
    # 实例化一个图书对象，使用book.id查询该书籍数据
    print('[view book]' + id)
    book = Book.objects.filter(id=id)
    if len(book) == 1:
        book = book[0]
    else:
        print('[warning views bookinfo]')
    pic = Picture.objects.filter(bookid=id)
    # 建立空字典存储booklist
    if request.method == 'POST':
        img = Picture(image=request.FILES.get('img'))
        print('[pic]' + request.FILES.get('img').name)
        img.bookid = book
        type_list = ['.jpg', '.png', '.gif', '.webp']
        # 判断上传图片格式
        if os.path.splitext(request.FILES.get('img').name)[1].lower() in type_list:
            img.save()

    return render(request, 'bookInfo.html', {'book':book, 'pic':pic, 'usernow': usernow})



def cart(request):
    carts = Cart(request)
    dict_book = {}
    dict_book['carts'] = carts
    return render(request, 'cart.html', dict_book)

def add_to_cart(request, book_id, quantity, price):
    book = Book.objects.get(id=book_id)
    print('[11]',book.name ,book_id, quantity, price)
    cart = Cart(request)
    cart.add(book, price, quantity)
    return  HttpResponseRedirect(reverse('index'))


def remove_from_cart(request, product_id):
    book = Book.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(book)
    return HttpResponseRedirect(reverse('index'))


def checkUser(request):
    if 'username' in request.session:
        username = request.session['username']
    else:
        username = None
    return username

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


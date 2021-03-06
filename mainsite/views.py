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
    usernow = checkUser(request)
    print('[`0]')
    if 'username' not in request.session:
        print('[`1]')
        if request.method == 'POST':
            print('[`2]')
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
            return render(request, 'login.html', {"usernow":usernow})

    else:
        print('[`2]')
        return render(request, 'login.html', {'usernow': usernow})

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect(reverse('index'))

def register(request):
    from mainsite.models import User

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
    # if 'p' in request.GET:
    usernow = checkUser(request)

    books = Book.objects.get_queryset().order_by('id')
    # 增加分页功能, 10本图书分为一页
    paginator = Paginator(books, 4)
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
    dict_book['carts'] = Cart(request)
    for i in range(len(items)):

        if Picture.objects.filter(bookid=items[i].id):
            items[i].image = Picture.objects.filter(bookid=items[i].id)[0].image
        else:
            items[i].image = None
        if Discount.objects.filter(bookid=items[i].id):
            tmp = Discount.objects.filter(bookid=items[i].id)[0].sale
            items[i].discount = int((1 - tmp) * 100)
            print('[93]',items[i].price)
            items[i].price_discount = round(items[i].price * tmp, 2)
        else:
            items[i].discount = 0
    return render(request, 'index.html', dict_book)
    # else:
    #     return render(request,'index.html')






def listbooks(request):
    # if 'p' in request.GET:
    usernow = checkUser(request)

    books = Book.objects.get_queryset().order_by('id')
    # 增加分页功能, 10本图书分为一页
    paginator = Paginator(books, 6)
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


    for i in range(len(items)):

        if Picture.objects.filter(bookid=items[i].id):
            items[i].image = Picture.objects.filter(bookid=items[i].id)[0].image
        else:
            items[i].image = None
        if Discount.objects.filter(bookid=items[i].id):
            tmp = Discount.objects.filter(bookid=items[i].id)[0].sale
            items[i].discount = int((1 - tmp) * 100)
            print('[93]',items[i].price)
            items[i].price_discount = round(items[i].price * tmp, 2)
        else:
            items[i].discount = 0
            items[i].price_discount = items[i].price

        dict_book = {}
        dict_book['booklist'] = items
        dict_book['carts'] = Cart(request)
        dict_book['usernow'] = usernow

    return render(request, 'listbooks.html', dict_book)
    # else:
    #     return render(request,'index.html')

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
    print(pic)
    # 建立空字典存储booklist
    # if request.method == 'POST':
    # img = Picture(image=request.FILES.get('img'))
    # print('[pic]' + request.FILES.get('img').name)
    # img.bookid = book
    # type_list = ['.jpg', '.png', '.gif', '.webp']
    # 判断上传图片格式
    # if os.path.splitext(request.FILES.get('img').name)[1].lower() in type_list:
    #     img.save()

    if Discount.objects.filter(bookid=id):
        tmp = Discount.objects.filter(bookid=id)[0].sale
        book.discount = round((tmp * 10),1)
        print('[93]', book.price)
        book.price_discount = round(book.price * tmp, 2)
    else:
        book.discount = 0

    category = Category.objects.filter(id=book.categoryid_id)[0]

    dict_book = {}
    dict_book['carts'] = Cart(request)
    dict_book['usernow'] = checkUser(request)
    dict_book['book'] = book
    dict_book['pic'] = pic
    dict_book['category'] = category

    return render(request, 'bookdetail.html', dict_book)



def cart(request):
    carts = Cart(request)
    dict_book = {}
    dict_book['carts'] = carts
    dict_book['usernow'] = checkUser(request)
    return render(request, 'cart.html', dict_book)

def add_to_cart(request, book_id, quantity, price):
    book = Book.objects.get(id=book_id)

    print('[11]',book.name ,book_id, quantity, price)
    cart = Cart(request)

    # if Picture.objects.filter(bookid=book.id):
    #     image = Picture.objects.filter(bookid=book.id)[0].image
    # discount = 0
    price_discount = book.price

    if Discount.objects.filter(bookid=book_id):
        tmp = Discount.objects.filter(bookid=book_id)[0].sale
        price_discount = round(book.price * tmp, 2)

    cart.add(book, price_discount, quantity)
    print(cart.summary())
    return HttpResponseRedirect(reverse('index'))


def remove_from_cart(request, product_id):
    print('[rr]')
    book = Book.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(book)

    return HttpResponseRedirect(reverse('index'))

def remove_all_from_cart(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponseRedirect(reverse('index'))


def order(request):
    carts = Cart(request)
    if 'username' in request.session:
        # 形成订单，形成订单项
        print('订单')
        if carts.count() != 0:
            if request.method == 'POST':
                print('POST')
                user = User.objects.get(username=request.session['username'])
                name = request.POST['order_name']
                num = request.POST['order_num']
                city = request.POST['order_city']
                county = request.POST['order_county']
                address = request.POST['order_address']
                address_all = city + county + address
                print(address_all)
                create_order(name,address_all,num,user,carts)
                carts.clear()
                return HttpResponseRedirect(reverse('index'))
        else:
            pass

        dict_book = {}
        dict_book['carts'] = carts

        usernow = checkUser(request)
        dict_book['usernow'] = usernow
        items=[]
        for i in range(carts.count()):
            pic = Picture.objects.filter(bookid=id)
            # 建立空字典存储booklist
            # if request.method == 'POST':
            # img = Picture(image=request.FILES.get('img'))
            # print('[pic]' + request.FILES.get('img').name)
            # img.bookid = book
            # type_list = ['.jpg', '.png', '.gif', '.webp']
            # 判断上传图片格式
            # if os.path.splitext(request.FILES.get('img').name)[1].lower() in type_list:
            #     img.save()

        return render(request, 'order.html', dict_book)
    else:
        return HttpResponseRedirect(reverse('login'))


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

def create_order(name, address, phonenum,  buyer, cart):
    publish_obj = Order.objects.create(status='1', name=name, address=address, phonenum=phonenum, buyer=buyer)
    for item in cart:
        Orderitem.objects.create(orderid=publish_obj,
                                        bookid_id=item.product.id,
                                        price=item.product.price,
                                        quantity=item.quantity,
                                        sale=0.1,
                                        prices=item.total_price,
                                )
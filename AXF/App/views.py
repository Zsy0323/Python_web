import hashlib
import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect

from AXF.settings import BASE_DIR, MEDIA_ROOT
from .models import *


# 首页
def home(request):
    # 轮播数据
    wheels = MainWheel.objects.all()
    # 导航数据
    navs = MainNav.objects.all()
    # 必购数据
    mustbuy = MainMustbuy.objects.all()
    # shop数据
    shops = MainShop.objects.all()
    shop0 = shops.first()
    shop1_2 = shops[1:3]
    shop3_6 = shops[3:7]
    shop7_10 = shops[7:11]
    # 主要商品数据
    mainshows = MainShow.objects.all()
    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuy,
        'shop0': shop0,
        'shop1_2': shop1_2,
        'shop3_6': shop3_6,
        'shop7_10': shop7_10,
        'mainshows': mainshows,
    }
    return render(request, 'home/home.html', data)


# 闪购
def market(request):
    return redirect(reverse('App:marketwithparams', args=['104749', '0', '0']))


def market_with_params(request, typeid, typechildid, sortid):
    # 分类数据
    foodtypes = FoodType.objects.all()
    # 商品数据
    goods = Goods.objects.filter(categoryid=typeid)
    # 按照子分类筛选
    if typechildid != '0':
        goods = goods.filter(childcid=typechildid)

    # 获取当前主分类
    childnames = foodtypes.filter(typeid=typeid)
    child_type_list = []  # 存放子分类
    if childnames.exists():
        childtypes = childnames.first().childtypenames.split('#')
        for type in childtypes:
            type_list = type.split(':')
            child_type_list.append(type_list)

    # 排序规则
    if sortid == '0':
        pass
    elif sortid == '1':
        goods = goods.order_by('-productnum')
    elif sortid == '2':
        goods = goods.order_by('-price')
    elif sortid == '3':
        goods = goods.order_by('price')

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods,
        'typeid': typeid,
        'child_type_list': child_type_list,
        'typechildid': typechildid,

    }
    return render(request, 'market/market.html', data)


# 购物车
def cart(request):
    # 是否登录
    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:login'))
    else:
        carts = Cart.objects.filter(user_id=userid)
        return render(request, 'cart/cart.html', {'carts': carts})


# 我的
def mine(request):
    data = {
        'name': '',
        'icon': '',
    }
    userid = request.session.get('userid', '')
    if userid:
        user = User.objects.get(id=userid)

        data['name'] = user.name
        data['icon'] = '/upload/icon/' + user.icon
    return render(request, 'mine/mine.html', data)


# 注册
def register(request):
    return render(request, 'user/register.html')


# 注册操作
def r_handle(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        # print(password)

        # 注册之前检验
        if len(username) < 6:
            data['status'] = 0
            data['msg'] = '输入不合法'
            return render(request, 'user/register.html', data)

        # 注册
        try:
            user = User()
            user.name = username
            user.password = password
            if icon:
                filename = random_file() + '.png'
                user.icon = filename

                filepath = os.path.join(MEDIA_ROOT, filename)
                with open(filepath, 'ab') as fp:
                    for part in icon.chunks():
                        fp.write(part)
                        fp.flush()

            else:
                user.icon = ''
            user.email = email
            user.save()

            # 保存session
            request.session['userid'] = user.id

            return redirect(reverse('App:mine'))
        except:
            return redirect(reverse('App:register'))
    return redirect(reverse('App:register'))


# 用户名检测
def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        users = User.objects.filter(name=username)
        if users.exists():

            return JsonResponse({'status': 0, 'msg': '用户名已存在'})
        else:
            return JsonResponse({'status': 1, 'msg': 'ok'})

    return JsonResponse({'status': -1, 'msg': '请求方式错误'})


# 随机文件名称
def random_file():
    u = str(uuid.uuid4())
    m = hashlib.md5()
    m.update(u.encode('utf-8'))
    return m.hexdigest()


# 推出登录
def logout(request):
    # 删除session
    request.session.flush()
    return redirect(reverse('App:mine'))


# 登录页面
def login(request):
    return render(request, 'user/login.html')


# 登录处理
def l_handle(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        users = User.objects.filter(name=username, password=password)
        if users.exists():
            request.session['userid'] = users.first().id
            return redirect(reverse('App:mine'))
        else:
            data['status'] = 0
            data['msg'] = '用户民或密码错误'
            return render(request, 'user/login.html', data)

    data['status'] = -1
    data['msg'] = '请求方式错误'
    return render(request, 'user/login.html', data)


# 加入购物车
def add_cart(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }
    # 判断用户是否登录
    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
        # return redirect(reverse('App:login'))
    else:
        if request.method == 'GET':
            goodsid = request.GET.get('goodsid')
            num = request.GET.get('num')
            # 先判断该商品是否已经存在
            cart1 = Cart.objects.filter(goods_id=goodsid, user_id=userid)

            if cart1.exists():
                new_num = cart1.first().num + int(num)
                cart1.update(num=new_num)
            else:
                # 添加到购物车
                cart = Cart()
                cart.user_id = userid
                cart.goods_id = goodsid
                cart.num = num
                cart.save()
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 数量增加
def add_num(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')

    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')
            cart = Cart.objects.get(id=cartid)
            cart.num += 1
            cart.save()
            data['num'] = cart.num
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


def reduce_num(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')

    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')
            cart = Cart.objects.get(id=cartid)
            if cart.num - 1 < 1:
                cart.num = 1
            else:
                cart.num -= 1
            cart.save()
            data['num'] = cart.num
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 删除按钮
def delbtn(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')
            cart = Cart.objects.get(id=cartid)
            del cart
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 勾选
def cart_select(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            cartid = request.GET.get('cartid')
            cart = Cart.objects.get(id=cartid)
            cart.is_select = not cart.is_select
            cart.save()
            data['is_select'] = cart.is_select
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 取消全选
def cart_selectall(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            action = request.GET.get('action')
            selects = request.GET.get('selects')
            selects_list = selects.split('#')
            if action == 'cancelselect':

                Cart.objects.filter(id__in=selects_list).update(is_select=False)

            else:
                Cart.objects.filter(id__in=selects_list).update(is_select=True)

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 生成订单
def order_add(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            #     先获取当前用户购物车勾选的商品
            carts = Cart.objects.filter(user_id=userid, is_select=True)

            order = Order()
            order.order_id = str(uuid.uuid4())
            order.user_id = userid
            order.save()

            total = 0
            for cart in carts:
                order_goods = OrderGoods()
                order_goods.goods_id = cart.goods_id
                order_goods.order_id = order.id
                order_goods.num = cart.num
                order_goods.price = cart.goods.price
                order_goods.save()

                total += order_goods.num * order_goods.price

            # 添加总价
            order.order_price = total
            order.save()

            data['orderid'] = order.id

        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 订单页面
def order(request, orderid):
    order = Order.objects.get(id=orderid)

    return render(request, 'order/order.html', {'order': order})


# 更改订单状态
def order_changestatus(request):
    data = {
        'status': 1,
        'msg': 'ok',
    }

    userid = request.session.get('userid', '')
    if not userid:
        data['status'] = 0
        data['msg'] = '未登录'
    else:
        if request.method == 'GET':
            orderid = request.GET.get('orderid')
            status = request.GET.get('status')

            # 修改订单状态
            Order.objects.filter(id=orderid).update(order_status=status)
        else:
            data['status'] = -1
            data['msg'] = '请求方式不正确'

    return JsonResponse(data)


# 待付款页面
def order_waitpay(request):
    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:mine'))
    else:
        orders = Order.objects.filter(user_id=userid,order_status='0')

        return render(request,'order/order_waitpay.html',{'orders':orders})


def order_paid(request):
    userid = request.session.get('userid', '')
    if not userid:
        return redirect(reverse('App:mine'))
    else:
        orders = Order.objects.filter(user_id=userid,order_status='1')

        return render(request,'order/order_paid.html',{'orders':orders})

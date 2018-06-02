from django.shortcuts import render,reverse,redirect
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
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuy,
        'shop0':shop0,
        'shop1_2':shop1_2,
        'shop3_6':shop3_6,
        'shop7_10':shop7_10,
        'mainshows':mainshows,
    }
    return render(request,'home/home.html', data)


# 闪购
def market(request):
    return redirect(reverse('App:marketwithparams', args=['104749']))


def market_with_params(request, typeid):
    # 分类数据
    foodtypes = FoodType.objects.all()
    # 商品数据
    goods = Goods.objects.filter(categoryid=typeid)

    data = {
        'foodtypes':foodtypes,
        'goods_list':goods,
        'typeid':typeid,
    }
    return render(request,'market/market.html', data)


# 购物车
def cart(request):
    return render(request,'cart/cart.html')


# 我的
def mine(request):
    return render(request,'mine/mine.html')


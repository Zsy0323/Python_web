from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^home/$', home, name='home'),

    url(r'^market/$', market, name='market'),
    url(r'^marketwithparams/(\d+)/(\d+)/(\d+)/$', market_with_params, name='marketwithparams'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^mine/$', mine, name='mine'),

    url(r'^register/$', register, name='register'),
    url(r'^rhandle/$', r_handle, name='r_handle'),
    url(r'^checkusername/$', check_username, name='check_username'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^lhandle/$', l_handle, name='l_handle'),
    url(r'^addcart/$', add_cart, name='add_cart'),
    url(r'^addnum/$', add_num, name='add_num'),
    url(r'^reducenum/$', reduce_num, name='reduce_num'),
    url(r'^delbtn/$', delbtn, name='delbtn'),
    url(r'^cartselect/$', cart_select, name='cart_select'),
    url(r'^cartselectall/$', cart_selectall, name='cart_selectall'),

    url(r'^orderadd/$', order_add, name='order_add'),
    url(r'^order/(\d+)/$', order, name='order'),
    url(r'^orderchangestatus/$', order_changestatus, name='order_changestatus'),
    url(r'^orderwaitpay/$', order_waitpay, name='order_waitpay'),
    url(r'^orderpaid/$', order_paid, name='order_paid'),

]
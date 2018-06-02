from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^home/$', home, name='home'),

    url(r'^market/$', market, name='market'),
    url(r'^marketwithparams/(\d+)/$', market_with_params, name='marketwithparams'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^mine/$', mine, name='mine'),

]
"""Advertiser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import shop, market, customer
from django.conf.urls import url

app_name = 'market'

urlpatterns = [
        path('', shop.IndexView.as_view(), name='homepage'),
        path('login/', market.LoginINAs, name='loginAs'),
        path('login/loginShop/', shop.loginShop, name="loginShop"),
        path('login/signupShop/', shop.signupShop, name="signupShop"),

        # path('login/loginShop/', shop.ShopLoginView.as_view(), name="loginShop"),


        # todo: create a federated login for shopvisitor
        path('login/signupCustomer/', customer.CustomerSignUpView.as_view(), name="signupCustomer"),
        path('login/loginCustomer/', customer.loginCustomer, name="loginCustomer"),


        path('edit_shop/', shop.edit_shop, name='edit_shop'),
        path('edit_customer/', customer.edit_customer, name='edit_customer'),


        # path('create_addvertisement/', shop.create_addvertisement, name='create_addvertisement'),
        # url(r'^delete_advertisement/(?P<pk>\d+)/$', shop.AdvertisementDelete.as_view(), name='delete_advertisement'),
        # url(r'^update_advertisement/(?P<pk>\d+)/$', shop.AdvertisementUpdate.as_view(), name='update_advertisement'),

        path('delete_advertisement/<int:pk>', shop.AdvertisementDelete.as_view(), name='delete_advertisement'),
        path('update_advertisement/<int:pk>', shop.AdvertisementUpdate.as_view(), name='update_advertisement'),
        path('create_advertisement/', shop.AdvertisementCreate.as_view(), name='create_advertisement'),

        path('check_follow_status/', market.checkFollowStatus, name='check_follow_status'),
        path('follow_shop/', market.shop_follow, name='follow_shop'),

        path('public_profile/<int:pk>', shop.ShopIndexView.as_view(), name='public_profile'),
        path('logout/', market.LogOUT, name='logout'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


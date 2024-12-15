from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('cart/', views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('register/',views.register,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),
    path('search/',views.search,name="search"),
    path('category/',views.category,name="category"),
    path('admin/',views.manage,name="manage"),
    path('detail_page',views.detail_page,name="detail"),
    path('contact/',views.contact,name="contact"),
    path('introduce/',views.introduce,name="introduce"),
]

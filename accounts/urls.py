from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('user/', views.userpage, name='userpage'),
    path('account/', views.accountsettings, name='account'),
    path('register/', views.register, name='register'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('create_order/<str:pk>/', views.CreateOrder, name='create_order'),
    path('update_order/<str:pk>/', views.UpdateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.DeleteOrder, name='delete_order'),
]
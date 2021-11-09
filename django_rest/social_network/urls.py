from django.urls import path
from django.conf.urls import *
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^submit_message/$', views.submit_message, name ='submit_message'),
    path('new_like/', views.new_like, name='new_like'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name= 'logout'),
]
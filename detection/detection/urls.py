from django.urls import path, re_path
from newsbot import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fakePatrol/', views.index, name='index'),
]
# app_name='newsbot'
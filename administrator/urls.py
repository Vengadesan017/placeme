from django.urls import path,include
from . import views

app_name = 'administrator'

urlpatterns = [
    path('', views.Dashboard,name='dashboard'),
    path('profile/',views.Profile,name='profile'),
    path('create-user/',views.CreateUser,name='create-user'),
    path('recruiters/',views.Recruiters,name='recruiters'),
    path('logs/',views.Logs,name='logs'),
    path('users/',views.Users,name='users'),


    
]
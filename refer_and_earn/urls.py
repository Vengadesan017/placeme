from django.urls import path,include
from . import views

app_name = 'refer_and_earn'

urlpatterns = [
    path('', views.Home,name='home')

]
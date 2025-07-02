from django.urls import path,include
from . import views


app_name = 'auth'


urlpatterns = [
    path('', views.AuthPage),
    path('login', views.LoginPage,name='login'),
    path('signup', views.SignupPage,name='signup'),
    path('logout', views.LogoutPage,name='logout'),    
    path('signup', views.AgentSignupPage,name='agent_signup'),
]


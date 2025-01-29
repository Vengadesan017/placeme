from django.urls import path,include
from . import views


app_name = 'auth'


urlpatterns = [
    path('', views.AuthPage),
    path('login', views.LoginPage,name='login'),
    path('signup', views.SignupPage,name='signup'),
    path('employer_login',views.EmployerLogin,name="employer_login"),
    path('employer_signup',views.EmployerSignup,name="employer_signup"),
    path('logout', views.LogoutPage,name='logout'),    
]


from django.urls import path,include
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('', views.SearchCandidates,name='home'),
    path('create-company',views.CreateCompany,name="create_company"),
    path('complete_kyc',views.CompleteKYC,name="complete_kyc"),
    path('profile/',views.Profile,name='profile'),
    path('create-job/',views.CreateJob,name='create_job'),
    path('create-user/',views.CreateUser,name='create_user'),
    path('applications/',views.Applications,name='applications'),
    path('post/',views.Post,name='post'),
    path('users/',views.Users,name='users'),
    path('employee-life-cycle/',views.EmployeeLifeCycle,name='employee_life_cycle'),
]

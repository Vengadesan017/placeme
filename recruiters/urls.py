from django.urls import path,include
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('', views.OpenSearch,name='home'),
    path('keyword-search', views.KeywordSearch,name='keyword_search'),
    path('create-company/',views.CreateCompany,name="create_company"),
    path('complete-kyc/',views.CompleteKYC,name="complete_kyc"),
    path('profile/',views.Profile,name='profile'),
    path('create-job/',views.CreateJob,name='create_job'),
    path('create-user/',views.CreateUser,name='create_user'),
    path('applications/',views.Applications,name='applications'),
    path('post/',views.Post,name='post'),
    path('users/',views.Users,name='users'),
    path('employee-info/',views.EmployeeLifeCycle,name='employee_info'),


    path('onboarding/',views.OfferingOnboaring,name='onboarding'),
    path('vacancy/',views.Vacancy,name='vacancy'),
    path('admin-control/',views.AdminControl,name='admin_control'),
]

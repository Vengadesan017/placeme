from django.urls import path
from . import views

app_name = 'job_seeker'

urlpatterns = [
    path('', views.Home,name='home'),
    path('profile/',views.Profile,name='profile'),
    path('notifications/',views.Notifications,name='notifications'),
    path('search/',views.Search,name='search'),
    path('job/',views.Job,name='job'),
    path('my-job/',views.MyJob,name='my-job'),
    path('apply/',views.Apply,name='apply'),
    path('bookmark/',views.Bookmark,name='bookmark'),
    path('status/<str:page>',views.Status,name='status'),
    path('onboarding/<int:onboarding_id>/<str:page>',views.OnboardingCandidate,name='onboarding'),
    
    # API
    path('api/search/',views.ApiSearch,name='api-search'),

]

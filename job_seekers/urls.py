from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'job_seeker'

urlpatterns = [
    path('', views.Home,name='home'),
    path('profile/',views.Profile,name='profile'),
    path('search/',views.Search,name='search'),
    path('job/',views.Job,name='job'),
    path('apply/',views.Apply,name='apply'),
    path('bookmark/',views.Bookmark,name='bookmark'),
    path('status/<str:page>/',views.Status,name='status'),
    path('status/<str:page>/<int:id>',views.Status,name='status'),
    path('onboarding/<int:onboarding_id>/<str:page>',views.OnboardingCandidate,name='onboarding'),
    
    # API
    path('api/search/',views.ApiSearch,name='api_search'),
    path('api/keyword/',views.ApiTitle,name='api_title'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
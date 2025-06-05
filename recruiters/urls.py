from django.urls import path,include
from . import views

app_name = 'recruiters'

urlpatterns = [
    path('', views.OpenSearch,name='home'),
    path('advance-search/', views.AdvanceSearch,name='advance_search'),
    path('find-candidates/', views.FindCandidates,name='find_candidates'),
    path('candidate/', views.Candidate,name='candidate'),
    path('create-company/',views.CreateCompany,name="create_company"),
    path('complete-kyc/',views.CompleteKYC,name="complete_kyc"),
    path('profile/',views.Profile,name='profile'),
    path('create-job/',views.CreateJob,name='create_job'),
    path('create-user/',views.CreateUser,name='create_user'),
    path('applications/',views.Applications,name='applications'),
    path('post/',views.Post,name='post'),
    path('post/draft/',views.PostDraft,name='post_draft'),
    path('create-post/',views.CreatePost,name='create_post'),
    path('users/',views.Users,name='users'),
    path('employees/',views.EmployeeLifeCycle,name='employees'),


    path('hiring-tracker/',views.HiringTracker,name='hiring_tracker'),
    path('position-manager/',views.PositionManager,name='position_manager'),
    path('admin-control/<str:page>',views.AdminControl,name='admin_control'),
    path('all-packages/ ',views.AllPackages,name='all_packages'),
    
    # API
    path('api/position-manager/',views.APIPositionManager,name='api_position_manager'),
    path('api/create-job-form/',views.APICreatePostForm,name='api_create_job_form'),
]

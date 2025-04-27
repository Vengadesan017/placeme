from functools import wraps
from django.shortcuts import redirect,render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.db.models import Prefetch
from django.db.models import Subquery,OuterRef
from django.db.models import Case, When, Value, F
from django.db.models import IntegerField
from .forms import CreateCompanyForm, CreateCompanyKYCForm, CreatePosition, CreateHireRequest, CreateJobs
from .models import Companies, Positions, HireRequests, Qualifications, Locations, Benefits, Jobs
from job_seekers.models import Candidates, Skills
from django.contrib import messages
from .serializers import HireRequestSerializer, PositionSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from django.http import JsonResponse
from rest_framework.response import Response

def is_recruiter(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            if request.user.is_recruiter: 
                return view_func(request, *args, **kwargs)
            messages.info(request, "You must rigister your company or Your company admin must add you as recruiter")
            return redirect('recruiters:create_company')  # Replace with your no-permission page
        messages.info(request, "Please login  or signup")
        return redirect('auth:employer_login')  # Replace with your no-permission page
    return _wrapped_view

def is_kyc(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            candidate = Candidates.objects.get(user=request.user)
            company = Companies.objects.get(candidate=candidate)
            if company.is_kyc_verified:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Your KYC verification is pending.")
                return redirect('recruiters:complete_kyc')  # Replace with your KYC verification page
        except (Candidates.DoesNotExist, Companies.DoesNotExist):
            messages.error(request, "You must be associated with a company.")
            return redirect('error_page')  # Replace with your error page
    return _wrapped_view


@login_required
def CreateCompany(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        if request.method == "POST":
            if 'create_company' in request.POST:
                form = CreateCompanyForm(request.POST)
                if form.is_valid():
                    form.save(candidate=candidate)
                    messages.info(request,'Your Company was successfully Registered.')
                    try:
                        user = request.user
                        user.is_recruiter = True
                        user.save()
                    except Exception as e:
                        messages.error(request, 'An error occurred while garding you a company admin access.')
                    return redirect('recruiters:complete_kyc') 
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')
        createForm = CreateCompanyForm()
        context = {
            'createForm': createForm,
            'candidate':candidate
        }
        return render(request,'recruiters/create_company.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


@is_recruiter
def CompleteKYC(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        if request.method == "POST":
            if 'upload_kyc' in request.POST:
                form = CreateCompanyKYCForm(request.POST, request.FILES,instance=company)
                if form.is_valid():
                    form.save()
                    messages.info(request,'Your KYC was successfully Registered.')
                    return redirect('recruiters:complete_kyc') 
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')
        KYCForm = CreateCompanyKYCForm()
        if company.is_kyc_verified:
            return redirect('recruiters:home') 
        context = {
            'KYCForm': KYCForm,
            'company':company
        }
        return render(request,'recruiters/complete_kyc.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


@is_recruiter
@is_kyc
def OpenSearch(request):
    candidate = Candidates.objects.get(user=request.user)
    company = Companies.objects.get(candidate=candidate)
    candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()
    context = {
        'titles': candidate_titles,
        'company':company
    }
    return render(request,'recruiters/open_search.html',context)

@is_recruiter
@is_kyc
def AdvanceSearch(request):
    candidate = Candidates.objects.get(user=request.user)
    company = Companies.objects.get(candidate=candidate)
    candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()
    context = {
        'titles': candidate_titles,
        'company':company
    }
    return render(request,'recruiters/advance_search.html',context)

@is_recruiter
@is_kyc
def FindCondidates(request):
    candidate = Candidates.objects.get(user=request.user)
    company = Companies.objects.get(candidate=candidate)
    candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()
    context = {
        'titles': candidate_titles,
        'company':company
    }
    return render(request,'recruiters/find_candidates.html',context)

@is_recruiter
@is_kyc
def HiringTracker(request):
    candidate = Candidates.objects.get(user=request.user)
    company = Companies.objects.get(candidate=candidate)
    context = {
        'company':company
    }
    return render(request,'recruiters/hiring_tracker.html',context)

@is_recruiter
@is_kyc
def PositionManager(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        if request.method == 'POST':
            if 'create_position' in request.POST:
                position_count = request.POST.get('count')
                position_title = request.POST.get('position_title')
                try:
                    position_count = int(position_count)
                    if position_count <= 0:
                        position_count = 1
                except ValueError:
                    position_count = 1

                for i in range(min(position_count,20)):
                    create_position_form = CreatePosition(request.POST)
                    if create_position_form.is_valid():
                        create_position_form.save(company=company,created_by=candidate)
                    else:
                        return JsonResponse({'error': create_position_form.errors})

                # messages.info(request, f"{position_count} new position for {position_title} role was successfully created")
                # messages.info(request, f"Let's create the hire request to create the job post")
                return JsonResponse({'info': f"{position_count} new position for {position_title} role was successfully created.Let's create the hire request to create the job post"})

            if 'create_hire_request' in request.POST:
                selected_positions = request.POST.get('position', '')

                # Fallback to legacy support if position_id is submitted directly
                if not selected_positions:
                    position_id = request.POST.get('position')
                    if position_id:
                        selected_positions = position_id

                position_ids = selected_positions.split(',') if selected_positions else []

                if not position_ids:
                    return JsonResponse({'error': 'No positions selected'}, status=400)

                created_requests = []

                for position_id in position_ids:
                    # Clone the POST data and inject the position_id
                    mutable_post = request.POST.copy()
                    mutable_post['position'] = position_id
    
                    create_HR_form = CreateHireRequest(mutable_post)
                    if create_HR_form.is_valid():
                        hire_request = create_HR_form.save(company=company, created_by=candidate)
                        created_requests.append(hire_request.hire_request_id)
                    else:
                        return JsonResponse({
                            'error': f'Invalid data for position {position_id}',
                            'form_errors': create_HR_form.errors
                        }, status=400)

                return JsonResponse({
                    'info': f"{len(created_requests)} Hire Request(s) created successfully.",
                    'created_ids': created_requests
                })
                # # position_count = request.POST.get('count')
                # positions = request.POST.getlist('positions')
                # # position_title = request.POST.get('position')
                # print(positions)
                # create_HR_form = CreateHireRequest(request.POST)
                # if create_HR_form.is_valid():
                #     create_HR_form.save(company=company,created_by=candidate)
                #     return JsonResponse({'info': "New Hire Request was successfully created. Let's create the job post to hire Candidates"})

                # else:
                #     return JsonResponse({'error': create_HR_form.errors})


        
        """
        Loading the data and forms
        """
        positions = Positions.objects.filter(company=company).prefetch_related('hirerequests_set') 
        # positions = Positions.objects.filter(company=company) \
        #     .prefetch_related(
        #         Prefetch('hirerequests_set', queryset=HireRequests.objects.filter(company=company).order_by('employee_id'))
        #     )
        # for position in positions:
        #     print("//////",position)
        #     for hire_request in position.hirerequests_set.all():
        #         print("======>",hire_request)

        # positions = Positions.objects.annotate(
        #     hire_request_id=Subquery(
        #         HireRequests.objects.filter(position=OuterRef('pk')).values('id')[:1]
        #     )
        # )
                
        # for position in positions:
        #     print(position.title, position.hire_request_id if position.hire_request_id else "None") 

        # Querying HireRequests and ordering them according to the specified logic
        hire_requests = HireRequests.objects.filter(company=company) \
            .annotate(
            # Create a custom field to sort by `employee_id` being null or not
            employee_id_null=Case(
                When(employee_id__isnull=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
                )
            ) \
            .order_by('employee_id_null', 'deadline') 

        excluded_position_ids = hire_requests.values_list('position_id', flat=True)
        positions = Positions.objects.filter(company=company) \
            .exclude(position_id__in=excluded_position_ids)

        create_hire_request = CreateHireRequest(company=company)
    
                
        context = {
            'company':company,
            'positions':positions,
            'hire_requests':hire_requests,
            'form':CreatePosition(),
            'create_hire_request':create_hire_request
        }
        return render(request,'recruiters/position_manager.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@is_recruiter
@is_kyc
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated]) 
def APIPositionManager(request):


    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)

        positions = Positions.objects.filter(company=company).prefetch_related('hirerequests_set') 

        # Querying HireRequests and ordering them according to the specified logic
        hire_requests = HireRequests.objects.filter(company=company) \
            .annotate(
            # Create a custom field to sort by `employee_id` being null or not
            employee_id_null=Case(
                When(employee_id__isnull=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
                )
            ) \
            .order_by('employee_id_null', 'deadline') 

        excluded_position_ids = hire_requests.values_list('position_id', flat=True)
        positions = Positions.objects.filter(company=company) \
            .exclude(position_id__in=excluded_position_ids)

        # 3. Optional: get helper/form data
        # create_hire_request = CreateHireRequest(company=company)

        # 4. Serialize and return
        return Response({
            'hire_requests': HireRequestSerializer(hire_requests, many=True).data,
            'positions': PositionSerializer(positions, many=True).data
            # 'create_hire_request': create_hire_request
        })
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
        
@is_recruiter
@is_kyc
def AdminControl(request,page):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        context = {
            'company':company,
            'page':page
        }
        return render(request,'recruiters/admin_control.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@is_recruiter
@is_kyc
def Applications(request):
    return HttpResponse("<h1>view the Candidate's Applications</h1>")

@is_recruiter
@is_kyc
def Post(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        posts = Jobs.objects.filter(company=company, is_draft=False).order_by('-created_at')
        # if request.method == "POST":
        #     if 'upload_kyc' in request.POST:
        #         form = CreateCompanyKYCForm(request.POST, request.FILES,instance=company)
        #         if form.is_valid():
        #             form.save()
        #             messages.info(request,'Your KYC was successfully Registered.')
        #             return redirect('recruiters:complete_kyc') 
        #         else:
        #             print("Form errors:", form.errors)
        #             messages.error(request, 'Please enter the valid data')
        # KYCForm = CreateCompanyKYCForm()
        context = {
            # 'KYCForm': KYCForm,
            'company':company,
            'posts':posts
        }
        return render(request,'recruiters/post.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@is_recruiter
@is_kyc
def PostDraft(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        posts = Jobs.objects.filter(company=company, is_draft=True).order_by('-created_at')
        # if request.method == "POST":
        #     if 'upload_kyc' in request.POST:
        #         form = CreateCompanyKYCForm(request.POST, request.FILES,instance=company)
        #         if form.is_valid():
        #             form.save()
        #             messages.info(request,'Your KYC was successfully Registered.')
        #             return redirect('recruiters:complete_kyc') 
        #         else:
        #             print("Form errors:", form.errors)
        #             messages.error(request, 'Please enter the valid data')
        # KYCForm = CreateCompanyKYCForm()
        context = {
            # 'KYCForm': KYCForm,
            'company':company,
            'posts':posts
        }
        return render(request,'recruiters/post_draft.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@is_recruiter
@is_kyc
def CreatePost(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        
        if request.method == 'POST':
            form = CreateJobs(request.POST, company = company)
            if form.is_valid():
                job = form.save(commit=False,company=company,created_by=candidate)
                
                action = request.POST.get('action')
                if action == 'draft':
                    job.is_draft = True
                elif action == 'publish':
                    job.is_draft = False
                    
                job.save()  

                # # Handle the dynamic qualifications and skills
                # new_qualifications = request.POST.getlist('new_qualifications')  # Get the new qualifications from POST
                # new_locations = request.POST.getlist('new_locations')  # Get the new skills from POST
                # new_skills = request.POST.getlist('new_skills')  # Get the new skills from POST
                # new_benefits = request.POST.getlist('new_benefits')  # Get the new skills from POST

                # # Handle new qualifications
                # for qual_name in new_qualifications:
                #     try:
                #         qualification, created = Qualifications.objects.get_or_create(qualification=qual_name, created_by = candidate)
                #         job.qualifications.add(qualification)  # Add the qualification to the job
                #     except Exception as e:
                #         messages.error(request, f"Error saving qualification '{qual_name}': {str(e)} but post is created with out Qualifications")
                #         return redirect('recruiters:create_post')

                # # Handle new location
                # for location_name in new_locations:
                #     try:
                #         location, created = Locations.objects.get_or_create(location=location_name, created_by = candidate)
                #         job.location_id.add(location)  # Add the location to the job
                #     except Exception as e:
                #         messages.error(request, f"Error saving Location '{location_name}': {str(e)} but post is created with out location")
                #         return redirect('recruiters:create_post')
                    
                # # Handle new benefits
                # for benefit_name in new_benefits:
                #     try:
                #         benefit, created = Benefits.objects.get_or_create(benefit=benefit_name, created_by = candidate)
                #         job.benefit_id.add(benefit)  # Add the benefits to the job
                #     except Exception as e:
                #         messages.error(request, f"Error saving benefit '{benefit_name}': {str(e)} but post is created with out benefits")
                #         return redirect('recruiters:create_post')
                # # Handle new skills
                # for skill_name in new_skills:
                #     try:
                #         skill, created = Skills.objects.get_or_create(skill=skill_name, created_by = candidate)
                #         job.skills.add(skill)  # Add the skill to the job
                #     except Exception as e:
                #         messages.error(request, f"Error saving skill '{skill_name}': {str(e)} but post is created with out key skills")
                #         return redirect('recruiters:create_post')

                # # Now save any other many-to-many relationships through the form
                form.save_m2m()

                if action == 'draft':
                    messages.info(request, "Saved as Draft.")
                    return redirect('recruiters:post_draft')
                elif action == 'publish':
                    messages.info(request, "Job Published.")
                    return redirect('recruiters:post')
                else:
                    messages.error(request, "Job post did't able to save")
                    # redirect('recruiters:create_post')
                # messages.info(request, "Saved as Draft." if action == 'draft' else "Job Published.")
                # return redirect(f"{reverse('job_seeker:job')}?r={job.slug}")
                
            else:
                messages.error(request,form.errors)
                return redirect('recruiters:create_post')
        context = {
            # 'KYCForm': KYCForm,
            'company':company,
            'form' : CreateJobs(request.POST or None, company=company)
        }
        return render(request,'recruiters/post_create.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
@is_recruiter
@is_kyc
def CreateJob(request):
    return HttpResponse("<h1>CreateJob</h1>")

@is_recruiter
@is_kyc
def Users(request):
    return HttpResponse("<h1>view or edit Users</h1>")

@is_recruiter
@is_kyc
def CreateUser(request):
    return HttpResponse("<h1>CreateUsers</h1>")

@is_recruiter
@is_kyc
def Profile(request):
    return HttpResponse("<h1>view or edit profile</h1>")

@is_recruiter
@is_kyc
def EmployeeLifeCycle(request):
    candidate = Candidates.objects.get(user=request.user)
    company = Companies.objects.get(candidate=candidate)
    context = {
        'company':company
    }
    return render(request,'recruiters/employee_info.html',context)
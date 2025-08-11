
from django.shortcuts import redirect,render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib import messages

from django.db.models import Prefetch
from django.db.models import Subquery,OuterRef
from django.db.models import Case, When, Value, F, CharField
from django.db.models import IntegerField
from django.db.models import Count, Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import CreateCompanyForm, CreateCompanyKYCForm, CreatePosition, CreateHireRequest, CreateJobs, \
    PositionGroupForm
from .models import Companies, Positions, HireRequests, Qualifications, Locations, Benefits, Jobs, \
    PositionGroup
from job_seekers.models import Candidates, Skills, SpecificationForEdu, JobApplications, UserLanguages, \
    Employment, EducationMap
from .serializers import HireRequestSerializer, PositionSerializer, LocationSerializer, BenefitSerializer,\
    SkillSerializer, QualificationSerializer
from .services import build_candidate_query
from .decorators import is_kyc, is_recruiter
from job_seekers.utils import form_errors_to_messages, form_errors_to_messages_htmx

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from django.http import JsonResponse

from django.utils.http import url_has_allowed_host_and_scheme
import logging

logger = logging.getLogger('recruiter_logger')


# check the query num
from django.db import connection, reset_queries
import time



@login_required
def CreateCompany(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        createForm = CreateCompanyForm()
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
                    form_errors_to_messages(request, form)
                    createForm = form
        
        context = {
            'createForm': createForm,
            'candidate':candidate
        }
        return render(request,'recruiters/create_company.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
def CompleteKYC(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        KYCForm = CreateCompanyKYCForm()
        if request.method == "POST":
            if 'upload_kyc' in request.POST:
                form = CreateCompanyKYCForm(request.POST, request.FILES,instance=company)
                if form.is_valid():
                    form.save()
                    messages.info(request,'Your KYC was successfully Registered.')
                    return redirect('recruiters:complete_kyc') 
                else:
                    print("Form errors:", form.errors)
                    form_errors_to_messages(request, form)
                    KYCForm = form
        if company.is_kyc_verified:
            return redirect('recruiters:home') 
        context = {
            'KYCForm': KYCForm,
            'company':company
        }
        return render(request,'recruiters/complete_kyc.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def OpenSearch(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()
        context = {
            'titles': candidate_titles,
            'company':company
        }
        return render(request,'recruiters/keyword_search.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def AdvanceSearch(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()
        context = {
            'titles': candidate_titles,
            'company':company
        }
        return render(request,'recruiters/advance_search.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def AllCandidates(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()

        query = request.GET.get('q', '').strip()

        if query:
            # candidates = Candidates.objects.all()
            q_object = build_candidate_query(query)
            # candidates = candidates.filter(q_object).prefetch_related(
            #     Prefetch('employment_company', queryset=Employment.objects.select_related('type_id')),
            #     Prefetch('candidate_to_edu_map', queryset=EducationMap.objects.select_related('edu_id', 'type_id')),
            #     Prefetch('user_language', queryset=UserLanguages.objects.select_related('language_id'))
            # )
            candidates = Candidates.objects.filter(q_object).prefetch_related(
                Prefetch(
                    'employment_company',  # Assuming correct related_name in Employment
                    queryset=Employment.objects.select_related('type_id').order_by(F('dol').asc(nulls_first=True)),
                    to_attr='my_employment'
                ),
                Prefetch(
                    'candidate_to_edu_map',
                    queryset=EducationMap.objects.select_related('edu_id', 'type_id').order_by(F('year_of_passing').asc(nulls_first=True)),
                    to_attr='my_education'
                ),
                Prefetch(
                    'user_language',
                    queryset=UserLanguages.objects.select_related('language_id'),
                    to_attr='my_language'
                )
            )

        context = {
            'titles': candidate_titles,
            'candidates':candidates,
            'company':company
        }
        return render(request,'recruiters/all_candidates.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def MyCandidates(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        candidate_titles = Candidates.objects.values_list('present_designation', flat=True).distinct()
        position_grp_obj = PositionGroup.objects.filter(company=company)
        context = {
            'titles': candidate_titles,
            'company':company,
            'position_grp_obj': position_grp_obj
        }
        return render(request,'recruiters/my_candidates.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def Candidate(request, candidate_uuid = None):
    try:
        if candidate_uuid is None:
            return redirect('recruiters:home')
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        candidate = get_object_or_404(Candidates, candidate_uuid=candidate_uuid)
        
        education = EducationMap.objects.filter(candidate=candidate).order_by('-year_of_passing')
        language = UserLanguages.objects.filter(candidate=candidate)
        employment = Employment.objects.filter(candidate=candidate).order_by('-dol')


        skills_list = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []
        location_list = [loc.strip() for loc in candidate.preferred_location.split(',')] if candidate.preferred_location else []
        context = {
            'company':company,
            'candidate': candidate,
            'skills_list': skills_list,
            'location_list': location_list,
            'my_education': education,
            'my_employment': employment,
            'my_languages': language
        }
        return render(request,'recruiters/candidate.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def Applicant(request, applicant_id = None):
    try:
        if applicant_id is None:
            return redirect('recruiters:home')
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        application = get_object_or_404(JobApplications, applicant_id=applicant_id)

        # Mark as viewed if not already
        if application.viewed_at is None:
            application.viewed_at = timezone.now()
            application.viewed_by = candidate
            application.save()
        
        education = EducationMap.objects.filter(candidate=candidate).order_by('-year_of_passing')
        language = UserLanguages.objects.filter(candidate=candidate)
        employment = Employment.objects.filter(candidate=candidate).order_by('-dol')


        skills_list = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []
        location_list = [loc.strip() for loc in candidate.preferred_location.split(',')] if candidate.preferred_location else []
        context = {
            'company':company,
            'candidate': candidate,
            'skills_list': skills_list,
            'location_list': location_list,
            'my_education': education,
            'my_employment': employment,
            'my_languages': language,
            'application': application
        }
        return render(request,'recruiters/applicant.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def MyApplicants(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)

        # Get query parameters
        status_filter = request.GET.get('status', '')
        job_id = request.GET.get('job_id', '')
        try:
            page = int(request.GET.get('page', 1))
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1

        try:
            page_size = int(request.GET.get('limit', 10))
        except (ValueError, TypeError):
            page_size = 10

        # Fetch jobs posted by the company
        company_jobs = Jobs.objects.filter(company=company)

        applications = JobApplications.objects.filter(job__in=company_jobs).order_by('-applied_date')

        if job_id:
            applications = applications.filter(job__job_id=job_id)

        if status_filter:
            applications = applications.filter(status=status_filter)

        # Paginate the filtered applications
        paginator = Paginator(applications, page_size)
        try:
            applications_page = paginator.get_page(page)
        except EmptyPage:
            applications_page = paginator.get_page(1)

        # Handle pagination info safely
        start_index = applications_page.start_index() if paginator.count > 0 else 0
        end_index = applications_page.end_index() if paginator.count > 0 else 0

        statuses = [
            'Applied', 'Viewed', 'Shortlisted', 'Interviewed', 'Selected',
            'Offered', 'Accepted', 'Rejected', 'Hired'
        ]

        context = {
            'applications': applications_page,
            'statuses': statuses,
            'status_filter': status_filter,
            'job_id': job_id,
            'posts': company_jobs,
            'total': paginator.count,
            'start_index': start_index,
            'end_index': end_index,
            'page_size': page_size,
            'page_range': paginator.page_range,
        }
        return render(request,'recruiters/my_applicants.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
@login_required
@is_recruiter
@is_kyc
def HiringTracker(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        # edit_candidate_in_hiring_form
        if request.method == 'POST' and request.htmx:
            context = {}
            template_name = None
            # -------- Form loading handlers --------
            if 'get_hire_request_form' in request.POST:
                pass
                # if pk := request.POST.get('get_hire_request_form'):
                #     instance = get_object_or_404(
                #         PositionGroup.objects.annotate(total_positions=Count('positions', distinct=True)),
                #         company=company,
                #         position_group_id=pk
                #     )   
                #     # Extract location IDs from the many-to-many field
                #     selected_location_ids = instance.locations.values_list('location_id', flat=True)
                #     selected_loc_ids_str = ','.join(str(id) for id in selected_location_ids)
                #     context['selected_loc_ids'] = selected_loc_ids_str
                #     context['position_form'] = PositionGroupForm(instance=instance)
                #     context['position_obj'] = instance
                # else:
                #     context['position_form'] = PositionGroupForm()
                # template_name = 'recruiters/htmx/positionSave.html'
            elif 'edit_candidate_in_hiring_form' in request.POST:
                if pk := request.POST.get('edit_candidate_in_hiring_form'):
                    instance = get_object_or_404(
                        HireRequests,
                        company=company,
                        hire_request_id=pk
                    )        
                    context['hire_request_form'] = CreateHireRequest(instance=instance)
                else:
                    return JsonResponse("Something went wrong, try again.", status=400)
                template_name = 'recruiters/htmx/hireRequestMapCandidateSave.html'
                
            if 'position_save' in request.POST:
                if pk := request.POST.get('position_save'):
                    instance = get_object_or_404(
                        PositionGroup.objects.annotate(total_positions=Count('positions', distinct=True)),
                        company=company,
                        position_group_id=pk
                    )
                    
                    try:
                        desired_count = int(request.POST.get('count', 1))
                        if desired_count < 1:
                            desired_count = 1
                    except ValueError:
                        desired_count = 1

                    form = PositionGroupForm(request.POST, instance=instance)
                    if form.is_valid():
                        group = form.save(commit=False)
                        group.position_code = instance.position_code
                        group.updated_by = candidate
                        group.save()
                        form.save_m2m()
                        
                        # Locations
                        new_locations_raw = request.POST.get('new_locations', '')
                        new_locations = [item.strip() for item in new_locations_raw.split(',') if item.strip()]
                        for location_name in new_locations:
                            try:
                                location, created = Locations.objects.get_or_create(location=location_name, created_by=candidate)
                                group.locations.add(location)
                            except Exception as e:
                                messages.error(request, f"Error saving location '{location_name}': {str(e)}")

                        # for location in form.cleaned_data.get('location_id', []):
                        #     group.locations.add(location)

                        existing_count = instance.total_positions
                        to_create = max(0, desired_count - existing_count)
                        for _ in range(0,min(to_create, 100)):
                            Positions.objects.create(position_group=group, created_by=candidate) 

                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
                else:
                    position_count = request.POST.get('count')
                    # position_title = request.POST.get('position_title')
                    try:
                        position_count = int(position_count)
                        if position_count <= 0:
                            position_count = 1
                    except ValueError:
                        position_count = 1
                    form = PositionGroupForm(request.POST)
                    if form.is_valid():
                        cleaned = form.cleaned_data
                        # locations = cleaned['locations']
                        group_all = request.POST.get('group_all')

                        # Initialize locations list
                        locations = set(cleaned.get('locations', []))
                        
                        # Handle new locations
                        new_locations_raw = request.POST.get('new_locations', '')
                        new_locations = [item.strip() for item in new_locations_raw.split(',') if item.strip()]
                        for location_name in new_locations:
                            try:
                                location, _ = Locations.objects.get_or_create(location=location_name, created_by=candidate)
                                locations.add(location)
                            except Exception as e:
                                messages.error(request, f"Error saving location '{location_name}': {str(e)}")
                        
                        # Common fields
                        common_data = {
                            'company': company,
                            'position_title': cleaned['position_title'],
                            'jd': cleaned['jd'],
                            'budget': cleaned['budget'],
                            'budget_type': cleaned['budget_type'],
                            'department': cleaned['department'],
                            'cost_center': cleaned['cost_center'],
                            'Supervisor': cleaned['Supervisor'],
                            'hrbp': cleaned['hrbp'],
                            'hrms': cleaned['hrms'],
                            'division': cleaned['division'],
                            'created_by': candidate
                        }

                        if not group_all:
                            group = PositionGroup.objects.create(**common_data)
                            group.locations.set(locations)

                            for _ in range(0,min(position_count,100)):
                                position = Positions.objects.create(
                                    position_group=group,
                                    created_by=candidate
                                )                             
                        else:
                            for location in locations:
                                group = PositionGroup.objects.create(**common_data)
                                group.locations.set([location])  # only this location                
                                for _ in range(0,min(position_count,100)):
                                    position = Positions.objects.create(
                                        position_group=group,
                                        created_by=candidate
                                    )  
                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
            elif pk := request.POST.get('hire_request_map_candidate'):
                status = request.POST.get('status')
                instance = get_object_or_404(HireRequests, hire_request_id=pk)
                
                emp_id = False
                if instance.employee_id:
                    emp_id = instance.employee_id
                form = CreateHireRequest(request.POST, instance=instance)

                if form.is_valid():
                    hire_request = form.save(commit=False)



                    if emp_id:
                        hire_request.employee_id = emp_id



                    if status == 'offered':
                        hire_request.is_offered = True
                    elif status == 'approve':
                        hire_request.is_approve = True
                    elif status == 'hire':
                        hire_request.is_hire = True
                        hire_request.hire_date = timezone.now()
                    elif status == 'join':
                        hire_request.is_join = True
                    elif status == 'leave':
                        hire_request.is_leave = True
                        hire_request.leave_date = timezone.now()
                    elif status == 'reject':
                        hire_request.is_reject = True

                    hire_request.hire_request_code = instance.hire_request_code
                    hire_request.updated_by = candidate
                    hire_request.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)                
                        
        

            if not template_name:
                hire_request_obj = HireRequests.objects.filter(company=company).annotate(
                    status_order=Case(
                        When(is_reject=True, then=Value(5)),
                        When(is_leave=True, then=Value(3)), 
                        When(is_hire=True, then=Value(4)),
                        When(is_approve=True, then=Value(6)),
                        When(Q(employee_id__isnull=False) & Q(is_open=True), then=Value(7)),  # candidate needed
                        When(Q(employee_id__isnull=True) & Q(is_open=True) & Q(is_hire=False), then=Value(8)),  # candidate needed
                        When(Q(employee_id__isnull=True) & Q(is_open=False), then=Value(2)),  # candidate needed
                        When(is_open=False, then=Value(1)),   # show in last
                        default=Value(99),
                        output_field=IntegerField()
                    )
                ).order_by('status_order', '-created_at') 
                # position_grp_obj = PositionGroup.objects.filter(company=company)
                # context = {
                #     'company':company,
                #     'hire_request_obj':hire_requests
                # }

                context['hire_request_obj'] = hire_request_obj
                template_name = 'recruiters/htmx/hireRequestShow.html'
                
            # -------- Final HTMX return --------
            if template_name:
                return render(request, template_name, context)                    
    
    
        # 
        hire_request_obj = HireRequests.objects.filter(company=company).annotate(
            status_order=Case(
                When(is_reject=True, then=Value(5)),
                When(is_leave=True, then=Value(3)), 
                When(is_hire=True, then=Value(4)),
                When(is_approve=True, then=Value(6)),
                When(Q(employee_id__isnull=False) & Q(is_open=True), then=Value(7)),  # candidate needed
                When(Q(employee_id__isnull=True) & Q(is_open=True) & Q(is_hire=False), then=Value(8)),  # candidate needed
                When(Q(employee_id__isnull=True) & Q(is_open=False), then=Value(2)),  # candidate needed
                When(is_open=False, then=Value(1)),   # show in last
                default=Value(99),
                output_field=IntegerField()
            )
        ).order_by('status_order', '-created_at') 
        position_grp_obj = PositionGroup.objects.filter(company=company)
        context = {
            'company':company,
            'hire_request_obj':hire_request_obj,
            'position_grp_obj':position_grp_obj
        }
        return render(request,'recruiters/hiring_tracker.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def PositionManager(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)

        if request.method == 'POST' and request.htmx:
            context = {}
            template_name = None
            # -------- Form loading handlers --------
            if 'get_position_form' in request.POST:
                if pk := request.POST.get('get_position_form'):
                    instance = get_object_or_404(
                        PositionGroup.objects.annotate(total_positions=Count('positions', distinct=True)),
                        company=company,
                        position_group_id=pk
                    )   
                    # Extract location IDs from the many-to-many field
                    selected_location_ids = instance.locations.values_list('location_id', flat=True)
                    selected_loc_ids_str = ','.join(str(id) for id in selected_location_ids)
                    context['selected_loc_ids'] = selected_loc_ids_str
                    context['position_form'] = PositionGroupForm(instance=instance)
                    context['position_obj'] = instance
                else:
                    context['position_form'] = PositionGroupForm()
                template_name = 'recruiters/htmx/positionSave.html'
            elif 'edit_hire_request_form' in request.POST:
                if pk := request.POST.get('edit_hire_request_form'):
                    instance = get_object_or_404(
                        PositionGroup.objects.annotate(total_positions=Count('positions', distinct=True)),
                        company=company,
                        position_group_id=pk
                    )        
                    context['position_obj'] = instance
                else:
                    return JsonResponse("Something went wrong, try again.", status=400)
                template_name = 'recruiters/htmx/positionHireRequestSave.html'
                
            if 'position_save' in request.POST:
                if pk := request.POST.get('position_save'):
                    instance = get_object_or_404(
                        PositionGroup.objects.annotate(total_positions=Count('positions', distinct=True)),
                        company=company,
                        position_group_id=pk
                    )
                    
                    try:
                        desired_count = int(request.POST.get('count', 1))
                        if desired_count < 1:
                            desired_count = 1
                    except ValueError:
                        desired_count = 1

                    form = PositionGroupForm(request.POST, instance=instance)
                    if form.is_valid():
                        group = form.save(commit=False)
                        group.position_code = instance.position_code
                        group.updated_by = candidate
                        group.save()
                        form.save_m2m()
                        
                        # Locations
                        new_locations_raw = request.POST.get('new_locations', '')
                        new_locations = [item.strip() for item in new_locations_raw.split(',') if item.strip()]
                        for location_name in new_locations:
                            try:
                                location, created = Locations.objects.get_or_create(location=location_name, created_by=candidate)
                                group.locations.add(location)
                            except Exception as e:
                                messages.error(request, f"Error saving location '{location_name}': {str(e)}")

                        # for location in form.cleaned_data.get('location_id', []):
                        #     group.locations.add(location)

                        existing_count = instance.total_positions
                        to_create = max(0, desired_count - existing_count)
                        for _ in range(0,min(to_create, 100)):
                            Positions.objects.create(position_group=group, created_by=candidate) 

                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
                else:
                    position_count = request.POST.get('count')
                    # position_title = request.POST.get('position_title')
                    try:
                        position_count = int(position_count)
                        if position_count <= 0:
                            position_count = 1
                    except ValueError:
                        position_count = 1
                    form = PositionGroupForm(request.POST)
                    if form.is_valid():
                        cleaned = form.cleaned_data
                        # locations = cleaned['locations']
                        group_all = request.POST.get('group_all')

                        # Initialize locations list
                        locations = set(cleaned.get('locations', []))
                        
                        # Handle new locations
                        new_locations_raw = request.POST.get('new_locations', '')
                        new_locations = [item.strip() for item in new_locations_raw.split(',') if item.strip()]
                        for location_name in new_locations:
                            try:
                                location, _ = Locations.objects.get_or_create(location=location_name, created_by=candidate)
                                locations.add(location)
                            except Exception as e:
                                messages.error(request, f"Error saving location '{location_name}': {str(e)}")
                        
                        # Common fields
                        common_data = {
                            'company': company,
                            'position_title': cleaned['position_title'],
                            'jd': cleaned['jd'],
                            'budget': cleaned['budget'],
                            'budget_type': cleaned['budget_type'],
                            'department': cleaned['department'],
                            'cost_center': cleaned['cost_center'],
                            'Supervisor': cleaned['Supervisor'],
                            'hrbp': cleaned['hrbp'],
                            'hrms': cleaned['hrms'],
                            'division': cleaned['division'],
                            'created_by': candidate
                        }

                        if not group_all:
                            group = PositionGroup.objects.create(**common_data)
                            group.locations.set(locations)

                            for _ in range(0,min(position_count,100)):
                                position = Positions.objects.create(
                                    position_group=group,
                                    created_by=candidate
                                )                             
                        else:
                            for location in locations:
                                group = PositionGroup.objects.create(**common_data)
                                group.locations.set([location])  # only this location                
                                for _ in range(0,min(position_count,100)):
                                    position = Positions.objects.create(
                                        position_group=group,
                                        created_by=candidate
                                    )  
                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
            elif pk := request.POST.get('hire_request_create'):
                hire_request_count = request.POST.get('count')
                try:
                    hire_request_count = int(hire_request_count)
                    if hire_request_count <= 0:
                        hire_request_count = 1
                except ValueError:
                    hire_request_count = 1
                
                instance = get_object_or_404(PositionGroup, company=company, position_group_id=pk)
                if instance:
                    # Common fields
                    common_data = {
                        'company': company,
                        'position_group': instance,
                        'created_by': candidate
                    }
                    for _ in range(0,min(hire_request_count,100)):
                        hr = HireRequests.objects.create(**common_data)                         
                        
                        
                else:
                    return JsonResponse('No position found', status=400)


            if not template_name:
                position_groups = (
                    PositionGroup.objects.filter(company=company)
                    .annotate(
                        # Openings
                        total=Count(
                            'positions',
                            filter=Q(positions__is_open=True, positions__is_active=True),
                            distinct=True
                        ),
                        # Hired
                        hired=Count(
                            'position_grp_in_hr',
                            filter=Q(
                                    positions__is_open=True,
                                     positions__is_active=True,
                                     position_grp_in_hr__is_hire=True
                                     ),
                            distinct=True
                        ),
                        # In progess
                        inprogress=Count(
                            'position_grp_in_hr',
                            filter=Q(
                                positions__is_open=True,
                                positions__is_active=True,
                                position_grp_in_hr__is_open=True,
                                position_grp_in_hr__is_active=True,
                                position_grp_in_hr__is_hire=False
                            ),
                            distinct=True
                        ),
                        # pending
                        pending=Count(
                            'positions',
                            filter=Q(
                                positions__is_open=True,
                                positions__is_active=True,
                                positions__position_in_hr__isnull=True  # no hire request linked
                            ),
                            distinct=True
                        ),
                    )
                    .annotate(
                        pending=Coalesce(F('total') - F('inprogress') -F('hired'), Value(0))
                    )
                    .order_by('-pending', '-total', '-hired', '-inprogress')
                )


                context['position_groups'] = position_groups
                template_name = 'recruiters/htmx/positionShow.html'
                
            # -------- Final HTMX return --------
            if template_name:
                return render(request, template_name, context)                    

        if request.method == 'POST':
            if 'create_position' in request.POST:
                position_count = request.POST.get('count')
                # position_title = request.POST.get('position_title')
                try:
                    position_count = int(position_count)
                    if position_count <= 0:
                        position_count = 1
                except ValueError:
                    position_count = 1
                

                form = PositionGroupForm(request.POST)
                if form.is_valid():
                    cleaned = form.cleaned_data
                    locations = cleaned['locations']
                    group_all = request.POST.get('group_all')
                    
                    # Common fields
                    common_data = {
                        'company': request.user.company,
                        'position_title': cleaned['position_title'],
                        'jd': cleaned['jd'],
                        'budget': cleaned['budget'],
                        'department': cleaned['department'],
                        'cost_center': cleaned['cost_center'],
                        'Supervisor': cleaned['Supervisor'],
                        'hrbp': cleaned['hrbp'],
                        'hrms': cleaned['hrms'],
                        'division': cleaned['division'],
                        'created_by': candidate
                    }

                    if not group_all:
                        group = PositionGroup.objects.create(**common_data)
                        group.locations.set(locations)
                        for _ in range(min(position_count,100)):
                            position = Positions.objects.create(
                                position_group=group,
                                created_by=candidate
                            )   
                    else:
                        for location in locations:
                            group = PositionGroup.objects.create(**common_data)
                            group.locations.set([location])  # only this location                
                # 
                            for _ in range(min(position_count,100)):
                                position = Positions.objects.create(
                                    position_group=group,
                                    created_by=candidate
                                )                        
                


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
        position_grp = PositionGroup.objects.filter(company=company)
        if position_grp:
            for x in position_grp:
                positions = x.positions.all()
            # print(positions.positions.all())
        else:
            positions = []
            # ================================error here in showing data
            
        position_groups = (
            PositionGroup.objects.filter(company=company)
            .annotate(
                # Openings
                total=Count(
                    'positions',
                    filter=Q(positions__is_open=True, positions__is_active=True),
                    distinct=True
                ),
                # Hired
                hired=Count(
                    'position_grp_in_hr',
                    filter=Q(
                            positions__is_open=True,
                                positions__is_active=True,
                                position_grp_in_hr__is_hire=True
                                ),
                    distinct=True
                ),
                # In progess
                inprogress=Count(
                    'position_grp_in_hr',
                    filter=Q(
                        positions__is_open=True,
                        positions__is_active=True,
                        position_grp_in_hr__is_open=True,
                        position_grp_in_hr__is_active=True,
                        position_grp_in_hr__is_hire=False
                    ),
                    distinct=True
                ),
                # pending
                pending=Count(
                    'positions',
                    filter=Q(
                        positions__is_open=True,
                        positions__is_active=True,
                        positions__position_in_hr__isnull=True  # no hire request linked
                    ),
                    distinct=True
                ),
            )
            .annotate(
                pending=Coalesce(F('total') - F('inprogress') -F('hired'), Value(0))
            )
            .order_by('-pending', '-total', '-hired', '-inprogress')
        )
        # position_groups = PositionGroup.objects.filter(company=company)  \
        # .annotate(
        #     total_positions=Count('positions', distinct=True),
        #     total_hire_requests=Count('position_grp_in_hr', distinct=True),
        #     open_hire_requests=Count(
        #         'position_grp_in_hr',
        #         filter=Q(position_grp_in_hr__is_open=True),
        #         distinct=True
        #     ),
        #     active_hire_requests=Count(
        #         'position_grp_in_hr',
        #         filter=Q(position_grp_in_hr__is_active=True),
        #         distinct=True
        #     ),

        #     total_offered=Count(
        #         'position_grp_in_hr',
        #         filter=Q(position_grp_in_hr__is_offered=True),
        #         distinct=True
        #     ),
        #     total_joined=Count(
        #         'position_grp_in_hr',
        #         filter=Q(position_grp_in_hr__is_hire=True),
        #         distinct=True
        #     ),
        #     empty_position=Count(
        #         'positions',
        #         filter=Q(
        #             positions__is_open=True,
        #             positions__is_active=True
        #                     ),
        #         distinct=True
        #     ),

        #     hiring_need=Count(
        #         'position_grp_in_hr',
        #         filter=Q(
        #             position_grp_in_hr__is_open=True,
        #             position_grp_in_hr__is_active=True,
        #             position_grp_in_hr__employee_id__isnull=True,
        #             position_grp_in_hr__is_hire=False
        #         ),
        #         distinct=True
        #     )
        # ).order_by('-empty_position','-hiring_need')

        

        # hire_requests = HireRequests.objects.filter(company=company) \
        #     .annotate(
        #     # Create a custom field to sort by `employee_id` being null or not
        #     employee_id_null=Case(
        #         When(employee_id__isnull=True, then=Value(0)),
        #         default=Value(1),
        #         output_field=IntegerField()
        #         )
        #     ) \
        #     .order_by('employee_id_null', 'deadline') 

        # excluded_position_ids = hire_requests.values_list('position_id', flat=True)
        # positions = Positions.objects.filter(company=company) \
        #     .exclude(position_id__in=excluded_position_ids)

        # create_hire_request = CreateHireRequest(company=company)
    
                
        context = {
            'company':company,
            'position_grp':position_grp,
            'position_groups':position_groups,
            # 'hire_requests':hire_requests,
            # 'form':CreatePosition(),
            # 'create_hire_request':create_hire_request
        }
        return render(request,'recruiters/position_manager.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)



      
@login_required
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

@login_required
@is_recruiter
@is_kyc
def AllPackages(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        context = {
            'company':company,

        }
        return render(request,'recruiters/admin_control_all_packages.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def Applications(request):
    return HttpResponse("<h1>view the Candidate's Applications</h1>")

@login_required
@is_recruiter
@is_kyc
def Post(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        posts = Jobs.objects.filter(company=company, is_draft=False).annotate(
            applicant_count=Count('job_applications'),
            shortlisted_count=Count('job_applications', filter=Q(job_applications__status='Shortlisted')),
            offered_count=Count('job_applications', filter=Q(job_applications__status='Offered'))
        ).order_by('-created_at')
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

@login_required
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

@login_required
@is_recruiter
@is_kyc
def CreatePost(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        
        context = {}
        form = CreateJobs(company=company)
        if request.method == 'GET':
            position_id = request.GET.get('position')
            if position_id:
                position = get_object_or_404(PositionGroup, position_group_id=position_id, company=company)
                # Mapping fields from PositionGroup to CreateJobs form initial values
                initial = {
                    "position_grp": position.pk,  # This sets the ForeignKey to PositionGroup in Jobs model
                    "title": position.position_title,
                    "salary": position.budget,
                    "salary_type": position.budget_type,
                    "location_id": position.locations.all(),  # ManyToMany - can be pre-filled
                    "description": position.jd,
                }
                selected_location_ids = position.locations.values_list('location_id', flat=True)
                selected_loc_ids_str = ','.join(str(id) for id in selected_location_ids)
                context['selected_loc_ids'] = selected_loc_ids_str
                form = CreateJobs(initial=initial, company=company, position_group_id = position.position_group_id)
            
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
                form.save_m2m()



                # Qualifications
                new_qualifications_raw = request.POST.get('new_qualifications', '')
                new_qualifications = [item.strip() for item in new_qualifications_raw.split(',') if item.strip()]
                for qual_name in new_qualifications:
                    try:
                        qualification, created = SpecificationForEdu.objects.get_or_create(
                            name=qual_name, created_by=candidate)
                        job.qualifications.add(qualification)
                    except Exception as e:
                        messages.error(request, f"Error saving qualification '{qual_name}': {str(e)}")

                # Locations
                new_locations_raw = request.POST.get('new_locations', '')
                new_locations = [item.strip() for item in new_locations_raw.split(',') if item.strip()]
                for location_name in new_locations:
                    try:
                        location, created = Locations.objects.get_or_create(location=location_name, created_by=candidate)
                        job.location_id.add(location)
                    except Exception as e:
                        messages.error(request, f"Error saving location '{location_name}': {str(e)}")

                # Benefits
                new_benefits_raw = request.POST.get('new_benefits', '')
                new_benefits = [item.strip() for item in new_benefits_raw.split(',') if item.strip()]
                for benefit_name in new_benefits:
                    try:
                        benefit, created = Benefits.objects.get_or_create(benefit=benefit_name, Created_by=candidate)
                        job.benefit_id.add(benefit)
                    except Exception as e:
                        messages.error(request, f"Error saving benefit '{benefit_name}': {str(e)}")

                # Skills
                new_skills_raw = request.POST.get('new_skills', '')
                new_skills = [item.strip() for item in new_skills_raw.split(',') if item.strip()]
                for skill_name in new_skills:
                    try:
                        skill, created = Skills.objects.get_or_create(skill=skill_name, created_by=candidate)
                        job.skills.add(skill)
                    except Exception as e:
                        messages.error(request, f"Error saving skill '{skill_name}': {str(e)}")

                # If you want to include existing items from the multi-selects, you have to manually add them too:
                for qualification in form.cleaned_data.get('qualifications', []):
                    job.qualifications.add(qualification)
                for location in form.cleaned_data.get('location_id', []):
                    job.location_id.add(location)
                for benefit in form.cleaned_data.get('benefit_id', []):
                    job.benefit_id.add(benefit)
                for skill in form.cleaned_data.get('skills', []):
                    job.skills.add(skill)


                if action == 'draft':
                    messages.info(request, "Saved as Draft.")
                    return redirect('recruiters:post_draft')
                elif action == 'publish':
                    messages.info(request, "Job Published.")
                    return redirect('recruiters:post')
                else:
                    messages.error(request, "Job post did't able to save")
                    redirect('recruiters:create_post')
                # messages.info(request, "Saved as Draft." if action == 'draft' else "Job Published.")
                # return redirect(f"{reverse('job_seeker:job')}?r={job.slug}")
                
            else:
                form_errors_to_messages(request, form)
                form = form
                # return redirect('recruiters:create_post')


        

        context['company'] = company
        context['form'] = form
        return render(request,'recruiters/post_create.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
@is_recruiter
@is_kyc
def CreateJob(request):
    return HttpResponse("<h1>CreateJob</h1>")

@login_required
@is_recruiter
@is_kyc
def Users(request):
    return HttpResponse("<h1>view or edit Users</h1>")

@login_required
@is_recruiter
@is_kyc
def CreateUser(request):
    return HttpResponse("<h1>CreateUsers</h1>")

@login_required
@is_recruiter
@is_kyc
def Profile(request):
    return HttpResponse("<h1>view or edit profile</h1>")

@login_required
@is_recruiter
@is_kyc
def EmployeeLifeCycle(request):
    candidate = Candidates.objects.get(user=request.user)
    company = Companies.objects.get(candidate=candidate)
    context = {
        'company':company
    }
    return render(request,'recruiters/employee_info.html',context)
































# Api
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
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated]) 
def APICreatePostForm(request):
    try:
        reset_queries()
        start = time.time()
        
        # candidate = Candidates.objects.get(user=request.user)
        # company = Companies.objects.get(candidate=candidate)

        locations = Locations.objects.annotate(
            job_count=Count('location_map_jlm'),
            display_label=Case(
                When(district__name__isnull=True, then='location'),
                When(district__name='', then='location'),
                default=Concat('location', V(' ('), 'district__name', V(')')),
                output_field=CharField()
            )
        ).only('location_id', 'location', 'district__name').order_by('-job_count')

        skills = Skills.objects.annotate(
            job_count=Count('job_post_skills'),
            display_name=Case(
                When(domain__name__isnull=True, then='skill'),
                When(domain__name='', then='skill'),
                default=Concat('skill', V(' ('), 'domain__name', V(')')),
                output_field=CharField()
            )
        ).only('skill_id', 'skill', 'domain__name').order_by('-job_count')

        qualifications = SpecificationForEdu.objects.select_related('course').annotate(
            job_count=Count('qualification_map'),
            display_name=Case(
                When(name__isnull=True, then='course__name'),
                When(name='', then='course__name'),
                default=Concat('course__name', V(' '), 'name'),
                output_field=CharField()
            )
        ).order_by('-job_count')
        benefits = Benefits.objects.annotate(
            job_count=Count('benefit_map_jbm')
        ).order_by('-job_count')

        data = {
            'locations': LocationSerializer(locations, many=True).data,
            'skills': SkillSerializer(skills, many=True).data,
            'qualifications': QualificationSerializer(qualifications, many=True).data,
            'benefits': BenefitSerializer(benefits, many=True).data,
        }
        # print(f"Total Queries: {connection.queries}")
        print(f"Total Queries: {len(connection.queries)}")
        print(f"Time taken: {time.time() - start}")
        return Response(data)
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


@is_recruiter
@is_kyc
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated]) 
def APICreatePositionForm(request):
    try:
        reset_queries()
        start = time.time()
        
        # candidate = Candidates.objects.get(user=request.user)
        # company = Companies.objects.get(candidate=candidate)

        locations = Locations.objects.annotate(
            job_count=Count('location_map_jlm'),
            display_label=Case(
                When(district__name__isnull=True, then='location'),
                When(district__name='', then='location'),
                default=Concat('location', V(' ('), 'district__name', V(')')),
                output_field=CharField()
            )
        ).only('location_id', 'location', 'district__name').order_by('-job_count')

        # skills = Skills.objects.annotate(
        #     job_count=Count('job_post_skills'),
        #     display_name=Case(
        #         When(domain__name__isnull=True, then='skill'),
        #         When(domain__name='', then='skill'),
        #         default=Concat('skill', V(' ('), 'domain__name', V(')')),
        #         output_field=CharField()
        #     )
        # ).only('skill_id', 'skill', 'domain__name').order_by('-job_count')

        # qualifications = SpecificationForEdu.objects.select_related('course').annotate(
        #     job_count=Count('qualification_map'),
        #     display_name=Case(
        #         When(name__isnull=True, then='course__name'),
        #         When(name='', then='course__name'),
        #         default=Concat('course__name', V(' '), 'name'),
        #         output_field=CharField()
        #     )
        # ).order_by('-job_count')
        # benefits = Benefits.objects.annotate(
        #     job_count=Count('benefit_map_jbm')
        # ).order_by('-job_count')

        data = {
            'locations': LocationSerializer(locations, many=True).data,
            # 'skills': SkillSerializer(skills, many=True).data,
            # 'qualifications': QualificationSerializer(qualifications, many=True).data,
            # 'benefits': BenefitSerializer(benefits, many=True).data,
        }
        # print(f"Total Queries: {connection.queries}")
        print(f"Total Queries: {len(connection.queries)}")
        print(f"Time taken: {time.time() - start}")
        return Response(data)
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
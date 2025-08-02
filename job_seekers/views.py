from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, NoReverseMatch, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Case, When, Q, CharField
from django.db.models.functions import Concat
from django.db.models import Value as V, F
from django.db import transaction
from django.core.paginator import Paginator
from django.core.files.storage import default_storage

from credentials.models import Users
from recruiters.models import Jobs , Locations, Qualifications , OfferLetters, DistrictForLoc, StateForLoc
from .models import Candidates, JobApplications, Onboarding, EducationMap , UserLanguages,\
     LevelForEdu, CourseForEdu, Skills, Employment, Internship, Bookmarks, \
        Familys, SpecificationForEdu ,EducationType 
from .forms import CandidatePersonalUpdateForm, CandidateEducationUpdateForm, OnboardingCandidatePersonalForm,\
        OnboardingPersonalForm ,CandidateLanguageUpdateForm, CandidateLocationUpdateForm, CandidateCareerUpdateForm,\
        CandidateEmploymentUpdateForm, CandidateIntenshipUpdateForm, OnboardingFamilyForm, \
        ResumeForm, ProfileForm, IdentityForm, CandidateSummaryUpdateForm, CandidateSkillUpdateForm, OfferResponseForm
from .serializers import JobsCardSerializer, TitleSerializer, LocationSerializer
from .services import apply_filter_in_job,get_filter_from_job,search_job
from .decorators import is_onboarding
from .utils import form_errors_to_messages, form_errors_to_messages_htmx

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions


from django.utils.http import url_has_allowed_host_and_scheme
import logging

logger = logging.getLogger('job_seeker_logger')

# check the query num
from django.db import connection, reset_queries
import time


def safe_reverse(name):
    try:
        return reverse(name)
    except NoReverseMatch:
        return False

def Home(request):
    try:
        if request.user.is_authenticated:
            candidate = Candidates.objects.get(user=request.user)

            context = {
                "upload_resume_url": safe_reverse("job_seeker:profile"),
                "complete_profile_url": safe_reverse("job_seeker:profile"),
                "saved_url": reverse("job_seeker:status", kwargs={"page": "saved"}),
                "applied_url": reverse("job_seeker:status", kwargs={"page": "applied"}),
                "review_offer_url": safe_reverse("review_offer"),
                "onboarding_url": safe_reverse("review_offer"),
                "check_attendance_url": safe_reverse("check_attendance"),
                "apply_leave_url": safe_reverse("apply_leave"),
                "logout_url": safe_reverse("auth:logout"),
                "feedback_url": safe_reverse("job_seeker:home"),
            }
            onboarding_id = Onboarding.objects.filter(candidate=candidate).values_list('Onbording_id',flat=True).first()
            if onboarding_id:
                context['onboarding_url'] = reverse("job_seeker:onboarding", kwargs={
                    'onboarding_id': onboarding_id,
                    'page': 'personal'
                })
            offer_letter_id = JobApplications.objects.filter(
                candidate=candidate,
                offered_at__isnull=False,
                accepted_at__isnull=True,
                rejected_at__isnull=True
            ).values_list("id", flat=True).first()
            if offer_letter_id:
                context['review_offer_url'] = reverse("job_seeker:status", kwargs={
                    'page': 'offered',
                    'id': offer_letter_id
                })
        else:
            context = {}
        return render(request,'jobseeker/home.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
def Profile(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        if request.method == 'POST' and request.htmx:
            context = {}
            template_name = None
            # -------- Form loading handlers --------
            if 'get_personal_form' in request.POST:
                context['candidate_form'] = CandidatePersonalUpdateForm(instance=candidate)
                template_name = 'jobseeker/htmx/profilePersonalSave.html'
            elif 'get_summary_form' in request.POST:
                context['summary_form'] = CandidateSummaryUpdateForm(instance=candidate)
                template_name = 'jobseeker/htmx/profileSummarySave.html'
            elif 'get_education_form' in request.POST:
                if pk := request.POST.get('get_education_form'):
                    instance = get_object_or_404(EducationMap, candidate=candidate, edu_map_id=pk)
                    context['education_form'] = CandidateEducationUpdateForm(instance=instance)
                else:
                    context['education_form'] = CandidateEducationUpdateForm()
                template_name = 'jobseeker/htmx/profileEducationSave.html'
            elif 'get_skill_form' in request.POST:
                context['skills'] = Skills.objects.all()
                context['my_skills'] = candidate.skill
                template_name = 'jobseeker/htmx/profileSkillSave.html'
            elif 'get_language_form' in request.POST:
                user_languages = UserLanguages.objects.filter(candidate=candidate)
                context['my_languages'] = user_languages
                if not user_languages.exists():
                    context['language_form'] = CandidateLanguageUpdateForm()
                template_name = 'jobseeker/htmx/profileLanguageModal.html'
            elif 'get_location_form' in request.POST:
                context['states'] = StateForLoc.objects.all()
                context['districts'] = DistrictForLoc.objects.all()
                context['my_location'] = candidate.preferred_location
                template_name = 'jobseeker/htmx/profileLocationSave.html'
            elif 'get_employment_form' in request.POST:
                if pk := request.POST.get('get_employment_form'):
                    instance = get_object_or_404(Employment, candidate=candidate, work_company_id=pk)
                    context['employment_form'] = CandidateEmploymentUpdateForm(instance=instance)
                else:
                    context['employment_form'] = CandidateEmploymentUpdateForm()
                template_name = 'jobseeker/htmx/profileEmploymentSave.html'
            elif 'get_career_form' in request.POST:
                context['career_form'] = CandidateCareerUpdateForm(instance=candidate)
                template_name = 'jobseeker/htmx/profileCareerSave.html'
            elif 'get_resume_form' in request.POST:
                template_name = 'jobseeker/htmx/profileResumeSave.html'
            elif 'get_profile_form' in request.POST:
                template_name = 'jobseeker/htmx/profilePictureSave.html'
                
                
            if 'personal_save' in request.POST:
                form = CandidatePersonalUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)


                context['candidate'] = candidate
                template_name = 'jobseeker/htmx/profilePersonalShow.html'
            elif 'summary_save' in request.POST:
                form = CandidateSummaryUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)
                context['candidate'] = candidate
                template_name = 'jobseeker/htmx/profileSummaryShow.html'
            elif 'education_save' in request.POST or 'education_delete' in request.POST:
                if pk := request.POST.get('education_delete'):
                    instance = get_object_or_404(EducationMap, candidate=candidate, edu_map_id=pk)
                    instance.delete()
                else:
                    if pk := request.POST.get('education_save'):
                        instance = get_object_or_404(EducationMap, candidate=candidate, edu_map_id = pk)
                        form = CandidateEducationUpdateForm(request.POST, request.FILES,instance=instance)
                    else:
                        form = CandidateEducationUpdateForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
                context['my_education'] =  EducationMap.objects.filter(candidate=candidate).order_by(F('year_of_passing').asc(nulls_first=True))
                template_name = 'jobseeker/htmx/profileEducationShow.html'
            elif 'skill_save' in request.POST:
                form = CandidateSkillUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)
                context['skills_list'] = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []
                template_name = 'jobseeker/htmx/profileSkillShow.html'    
            elif 'save_language' in request.POST or 'edit_language' in request.POST or 'delete_language' in request.POST or 'add_row_lang' in request.POST:      
                context['language_form'] = CandidateLanguageUpdateForm()
                add_row = False
                if 'save_language' in request.POST:
                    if pk := request.POST.get('save_language'):
                        print(pk)
                        instance = get_object_or_404(UserLanguages, candidate=candidate, user_language_id=pk)
                        form = CandidateLanguageUpdateForm(request.POST,instance=instance)
                    else:
                        form = CandidateLanguageUpdateForm(request.POST)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
                elif 'edit_language' in request.POST:
                    if pk := request.POST.get('edit_language'):
                        instance = get_object_or_404(UserLanguages, candidate=candidate, user_language_id=pk)
                        context['language_form'] = CandidateLanguageUpdateForm(instance=instance)
                elif 'delete_language' in request.POST:
                    if pk := request.POST.get('delete_language'):
                        instance = get_object_or_404(UserLanguages, candidate=candidate, user_language_id=pk)
                        instance.delete()
                elif 'add_row_lang' in request.POST:
                    add_row = True
                context['my_languages'] = UserLanguages.objects.filter(candidate=candidate)
                context['add_row'] = add_row
                template_name = 'jobseeker/htmx/profileLanguageTable.html'
            elif 'location_save' in request.POST:
                form = CandidateLocationUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)
                context['location_list'] = [loc.strip() for loc in candidate.preferred_location.split(',')] if candidate.preferred_location else []
                template_name = 'jobseeker/htmx/profileLocationShow.html'    
            elif 'employment_save' in request.POST or 'employment_delete' in request.POST:
                if pk := request.POST.get('employment_delete'):
                    instance = get_object_or_404(Employment, candidate=candidate, work_company_id=pk)
                    instance.delete()
                else:
                    if pk := request.POST.get('employment_save'):
                        instance = get_object_or_404(Employment, candidate=candidate, work_company_id = pk)
                        form = CandidateEmploymentUpdateForm(request.POST, request.FILES,instance=instance)
                    else:
                        form = CandidateEmploymentUpdateForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        errors = form_errors_to_messages_htmx(form, level='error')
                        return JsonResponse(errors, status=400)
                context['my_employment'] =  Employment.objects.filter(candidate=candidate).order_by(F('dol').asc(nulls_first=True))
                template_name = 'jobseeker/htmx/profileEmploymentShow.html'
            elif 'career_save' in request.POST:
                form = CandidateCareerUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)
                context['candidate'] = candidate
                template_name = 'jobseeker/htmx/profileCareerShow.html'
            elif 'resume_save' in request.POST:
                form = ResumeForm(request.POST, request.FILES, instance= candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)
                context['candidate'] = candidate
                template_name = 'jobseeker/htmx/profileResumeShow.html'
            elif 'profile_pic_save' in request.POST:
                form = ProfileForm(request.POST, request.FILES, instance= candidate)
                if form.is_valid():
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors = form_errors_to_messages_htmx(form, level='error')
                    return JsonResponse(errors, status=400)
                context['candidate'] = candidate
                template_name = 'jobseeker/htmx/profilePictureShow.html'
                
            # -------- Final HTMX return --------
            if template_name:
                return render(request, template_name, context)                    
            else :
                return redirect("job_seeker:profile")
                    

        education = EducationMap.objects.filter(candidate=candidate).order_by(F('year_of_passing').asc(nulls_first=True))
        language = UserLanguages.objects.filter(candidate=candidate)
        employment = Employment.objects.filter(candidate=candidate).order_by(F('dol').asc(nulls_first=True))

        levels = list(LevelForEdu.objects.all().values('level_id', 'name'))
        courses = list(CourseForEdu.objects.all().values('course_id', 'name', 'level_id'))
        specs = list(SpecificationForEdu.objects.all().values('specification_id', 'name', 'course_id'))

        skills_list = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []
        location_list = [loc.strip() for loc in candidate.preferred_location.split(',')] if candidate.preferred_location else []
        context = {
            'candidate': candidate,
            'skills_list': skills_list,
            'location_list': location_list,
            'my_education': education,
            'my_employment': employment,
            'my_languages': language,
            'levels':levels,
            'courses':courses,
            'specs':specs,

        }
        return render(request,'jobseeker/profile.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def Search(request):
    try:
        keyword1 = request.GET.get('q', '')
        keyword2 = request.GET.get('p', '')        
        page_number = request.GET.get('page', 2)
        if request.user.is_authenticated:
            candidate = Candidates.objects.get(user=request.user)
        else:
            candidate = False
        jobs = search_job(request,keyword1,keyword2,page_number,candidate)
        if not jobs:
            context = {
                'page_obj': False
            }
            return render(request, 'jobseeker/jobs.html', context)
        

        # Apply Pagination
        paginator = Paginator(jobs, 10)  # Show 20 jobs per page
        page_obj = paginator.get_page(page_number)

        # Get Filter data to show in side bar
        filters = get_filter_from_job(jobs)

        context = {
            'page_obj': page_obj,
            'keyword1': keyword1,
            'keyword2': keyword2,
            'filters' : filters
        }
        return render(request, 'jobseeker/jobs.html', context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


def Job(request):
    try:
        job_slug = request.GET.get('r', '')
        job = Jobs.objects.get(slug=job_slug)

        # Increment the view count atomically
        Jobs.objects.filter(pk=job.pk).update(views=F('views') + 1)

        # Refresh the object to get updated view count if needed
        job.refresh_from_db()
        if request.user.is_authenticated:
            login = True
            check_applied = JobApplications.objects.filter(candidate=Candidates.objects.get(user=request.user), job=job.job_id)  
            if check_applied.exists():
                applied = True
            else:
                applied = False
        else:
            applied = False
            login = False 
        context = {
            'job': job,
            'applied': applied,
            'login':login
        }
        return render(request,'jobseeker/job.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


@login_required
def Apply(request):
    try:
        if request.method == 'POST':
            if "apply-job" in request.POST:
                slug = request.POST.get('slug') 
                title = request.POST.get('title') 
                job = Jobs.objects.get(slug=slug)
                candidate = Candidates.objects.get(user=request.user)
                JobApplications.objects.create(
                    candidate=candidate,
                    job=job
                )
                job.increment_applied_count()
                messages.info(request, f'You have successfully applied to {title} job')
                referer_url = request.META.get('HTTP_REFERER')
                if referer_url:
                    return redirect(referer_url)
                else:
                    return redirect('job_seeker:home')
        return redirect('job_seeker:home')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@csrf_exempt
@login_required
def Bookmark(request):
    try:
        if request.method == 'POST':
            if "save_job" in request.POST:
                # slug = request.POST.get('slug') 
                slug = request.POST.get('slug') 
                job = Jobs.objects.get(slug=slug)
                candidate = Candidates.objects.get(user=request.user)
                exist = Bookmarks.objects.filter(job=job,candidate=candidate)
                if exist:
                    exist.delete()
                    messages.info(request, f'Job unsaved successfully.')
                    candidate.increment_bookmarks_count(False)
                elif candidate.bookmarks_count <15:
                    b = Bookmarks.objects.create(
                        candidate=candidate,
                        job=job
                    )
                    if b:
                        candidate.increment_bookmarks_count(True)
                        messages.info(request, f'Job saved successfully.')
                    else:
                        messages.info(request, f'Failed to save the job.')
                else :
                    messages.error(request, f'You have reached your bookmark limit (15). Please unsave an old job to add a new one.')  


                referer_url = request.META.get('HTTP_REFERER')
                if referer_url:
                    return redirect(referer_url)
                else:
                    return redirect('job_seeker:home')

        return redirect('job_seeker:home')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
@login_required
def Status(request, page, id=None):
    try:
        candidate=Candidates.objects.get(user=request.user)
        if request.method == "POST":
            job_application_id = request.POST.get('application_id')
            offer_letter_id = request.POST.get('offer_id')

            application = get_object_or_404(JobApplications, id=job_application_id, candidate=candidate)
            print(application)
            offer = get_object_or_404(OfferLetters, offers_id=offer_letter_id, application=application)
            print(offer)

            form = OfferResponseForm(request.POST, instance=offer)

            if form.is_valid():
                try:
                    with transaction.atomic():
                        offer = form.save(commit=False)
                        offer.is_acknowledged = True
                        if form.cleaned_data['accept']:
                            offer.approve_at = timezone.now()
                            offer.approve_by = candidate
                            application.status = 'Accepted'
                            application.accepted_at = timezone.now()
                        elif form.cleaned_data['decline']:
                            offer.approve_at = None
                            offer.approve_by = None
                            application.status = 'Rejected'
                            application.rejected_at = timezone.now()

                        offer.save()
                        application.save()

                        messages.success(request, "Your response has been recorded.")
                        return redirect('job_seeker:status', page='offered')

                except Exception as e:
                    print(f"[ERROR] {e}")
                    messages.error(request, "Something went wrong while processing your response.")
                    return redirect('job_seeker:status', page='offered')
            else:
                print("Form errors:", form.errors)
                form_errors_to_messages(request, form)
                return redirect("job_seeker:status", page='offered')
                
        job_status = False
        onboarding_id = False
        offer = False
        # Try to get job_status directly if id is provided
        if page == 'applied' and id:
            job_status = JobApplications.objects.filter(id=id, candidate=candidate).first()
        elif page == 'offered' and id:
            job_status = JobApplications.objects.filter(id=id, candidate=candidate).first()
            if job_status:
                onboarding_id = Onboarding.objects.filter(candidate=candidate, job_post=job_status.id).values_list('Onbording_id', flat=True).first()


        # Get job-related lists
        bookmarks = Bookmarks.objects.filter(candidate=candidate).values_list('job', flat=True)
        jobs = Jobs.objects.filter(job_id__in=bookmarks)
        job_applications = JobApplications.objects.filter(candidate=candidate)
        applied = job_applications.filter(offered_at__isnull=True)
        offered = job_applications.filter(offered_at__isnull=False)


        # Fallback job_status if not found above
        if not job_status:
            job_status = applied.first() if page == 'applied' else offered.first() if page == 'offered' else None
            if page == 'offered' and job_status:
                onboarding_id = Onboarding.objects.filter(candidate=candidate, job_post=job_status.id).values().first()

        # Mark offer as viewed (Optional)
        if job_status and page == 'offered' and job_status.offer_id:
            offer = job_status.offer_id
            if not offer.is_view:
                offer.is_view = True
                offer.viewed_at = timezone.now()
                offer.save()


        context = {
            'bookmarks': jobs,
            'applied': applied,
            'offered': offered,
            'job_status': job_status,
            'offer': offer,
            'onboarding_id':onboarding_id or False,
            'page': page, 
        }
        return render(request,'jobseeker/status.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)



@login_required
@is_onboarding
def OnboardingCandidate(request,onboarding_id, page):
    
    try:
        candidate = Candidates.objects.get(user=request.user)
        family_form = OnboardingFamilyForm()
        if request.method == 'POST':
            if 'personal' in request.POST:
                candidate_form = OnboardingCandidatePersonalForm(request.POST, request.FILES, instance=Candidates.objects.get(user=request.user))
                onboarding_form = OnboardingPersonalForm(request.POST, request.FILES, instance=Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id))
                page = "family"
                if not candidate_form.is_valid():
                    form_errors_to_messages(request, candidate_form, 'error')
                    page = "personal"
                else:
                    candidate_form.save()
                    # x(not cleaned_data.get(field) for field in ['firstname', 'lastname', 'dob', 'email']):
                if not onboarding_form.is_valid():
                    form_errors_to_messages(request, onboarding_form)
                    page = "personal"
                else:
                    onboarding_form.save()

            if 'save_language' in request.POST or 'edit_language' in request.POST or 'delete_language' in request.POST or 'add_row_lang' in request.POST:      
                lang_form = CandidateLanguageUpdateForm()
                add_row = False
                if 'save_language' in request.POST:
                    if pk := request.POST.get('save_language'):
                        instance = get_object_or_404(UserLanguages, candidate=candidate, user_language_id=pk)
                        form = CandidateLanguageUpdateForm(request.POST,instance=instance)
                    else:
                        form = CandidateLanguageUpdateForm(request.POST)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        form_errors_to_messages(request, form)
                elif 'edit_language' in request.POST:
                    if pk := request.POST.get('edit_language'):
                        instance = get_object_or_404(UserLanguages, candidate=candidate, user_language_id=pk)
                        lang_form = CandidateLanguageUpdateForm(instance=instance)
                elif 'delete_language' in request.POST:
                    if pk := request.POST.get('delete_language'):
                        instance = get_object_or_404(UserLanguages, candidate=candidate, user_language_id=pk)
                        instance.delete()
                elif 'add_row_lang' in request.POST:
                    add_row = True

                if request.htmx:
                    context = {
                        'onboarding_obj': Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id),
                        'language_form' : lang_form,
                        'languages': UserLanguages.objects.filter(candidate=candidate),
                        'add_row' : add_row
                    }

                    return render(request,"jobseeker/htmx/onboarding_language_table.html",context)
                else:
                    return redirect("job_seeker:onboarding",onboarding_id=onboarding_id,page='family')

            if 'edit_family' in request.POST or 'save_family' in request.POST or 'delete_family' in request.POST:
                family_form = OnboardingFamilyForm()
                if pk := request.POST.get('edit_family'):
                    if pk:
                        instance = get_object_or_404(Familys, candidate=candidate, family_member_id=pk)
                        family_form = OnboardingFamilyForm(instance=instance)
                elif pk := request.POST.get('delete_family'):
                    if pk:
                        instance = get_object_or_404(Familys, candidate=candidate, family_member_id=pk)
                        instance.delete()
                else:
                    pk = request.POST.get('save_family')
                    if pk and pk != "None": 
                        instance = get_object_or_404(Familys, candidate=candidate, family_member_id = pk)
                        form = OnboardingFamilyForm(request.POST,instance=instance)
                    else:
                        form = OnboardingFamilyForm(request.POST)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        form_errors_to_messages(request, form)

                if request.htmx:
                    context = {
                    'onboarding_obj': Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id),
                    'family_form' : family_form,
                    'my_family' : Familys.objects.filter(candidate=candidate),
                    }
                    return render(request,"jobseeker/htmx/onboarding_family_table.html",context)
                return redirect("job_seeker:onboarding",onboarding_id=onboarding_id,page='family')
            
            if 'edit_education' in request.POST or 'save_education' in request.POST or 'delete_education' in request.POST:
                education_form = CandidateEducationUpdateForm()
                if pk := request.POST.get('edit_education'):
                    instance = get_object_or_404(EducationMap, candidate=candidate, edu_map_id=pk)
                    education_form = CandidateEducationUpdateForm(instance=instance)
                elif pk := request.POST.get('delete_education'):
                    instance = get_object_or_404(EducationMap, candidate=candidate, edu_map_id=pk)
                    instance.delete()
                else:
                    pk = request.POST.get('save_education')
                    if pk and pk != "None": 
                        instance = get_object_or_404(EducationMap, candidate=candidate, edu_map_id = pk)
                        form = CandidateEducationUpdateForm(request.POST, request.FILES,instance=instance)
                    else:
                        form = CandidateEducationUpdateForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        form_errors_to_messages(request, form)
                if request.htmx:
                    context = {
                    'onboarding_obj': Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id),
                    'education_form' : education_form,
                    'my_education' : EducationMap.objects.filter(candidate=candidate),
                    }
                    
                    return render(request,"jobseeker/htmx/onboarding_edu_table.html",context)
                return redirect("job_seeker:onboarding",onboarding_id=onboarding_id,page='education')

            if 'edit_experience' in request.POST or 'save_experience' in request.POST or 'delete_experience' in request.POST:
                experience_form = CandidateEmploymentUpdateForm()
                if pk := request.POST.get('edit_experience'):
                    instance = get_object_or_404(Employment, candidate=candidate, work_company_id=pk)
                    experience_form = CandidateEmploymentUpdateForm(instance=instance)
                elif pk := request.POST.get('delete_experience'):
                    instance = get_object_or_404(Employment, candidate=candidate, work_company_id=pk)
                    instance.delete()
                else:
                    pk = request.POST.get('save_experience')
                    if pk and pk != "None": 
                        instance = get_object_or_404(Employment, candidate=candidate, work_company_id = pk)
                        form = CandidateEmploymentUpdateForm(request.POST, request.FILES,instance=instance)
                    else:
                        form = CandidateEmploymentUpdateForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        form_errors_to_messages(request, form)
                if request.htmx:
                    context = {
                    'onboarding_obj': Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id),
                    'experience_form' : experience_form,
                    'my_experience' : Employment.objects.filter(candidate=candidate),
                    }
                    return render(request,"jobseeker/htmx/onboarding_exp_table.html",context)
                return redirect("job_seeker:onboarding",onboarding_id=onboarding_id,page='experience')

            if 'complete_onboarding' in request.POST:
                onboarding = Onboarding.objects.get(pk=onboarding_id)
                company = onboarding.company  # adjust if job_post or company is linked differently

                if request.method == 'POST':
                    form = IdentityForm(request.POST, request.FILES, instance=onboarding, company=company)
                    if form.is_valid():
                        form.save()
                        # Redirect or message
                else:
                    form = IdentityForm(instance=onboarding, company=company)

                return redirect("job_seeker:home")

                    

                    

                # return render(request,'jobseeker/onboarding.html',context)

        candidate_form = OnboardingCandidatePersonalForm(instance=Candidates.objects.get(user=request.user))
        # onboarding_form = OnboardingPersonalForm(instance=Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id))
        onboarding = Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id)
        onboarding_form = OnboardingPersonalForm(instance=onboarding)
        
        language_form = CandidateLanguageUpdateForm()
        languages = UserLanguages.objects.filter(candidate=candidate)
        education = EducationMap.objects.filter(candidate=candidate)
        my_experience = Employment.objects.filter(candidate=candidate)
        my_family =Familys.objects.filter(candidate=candidate)
        company = onboarding.company

        education_form = CandidateEducationUpdateForm()
        experience_form = CandidateEmploymentUpdateForm()
        
        levels = list(LevelForEdu.objects.all().values('level_id', 'name'))
        courses = list(CourseForEdu.objects.all().values('course_id', 'name', 'level_id'))
        specs = list(SpecificationForEdu.objects.all().values('specification_id', 'name', 'course_id'))
        
        context = {
            'onboarding_obj':onboarding,
            'candidate': candidate_form,
            'onboarding': onboarding_form,
            'language_form':language_form,
            'languages':languages,
            'my_family': my_family,
            'family_form': family_form,
            'my_education':education,
            'my_experience':my_experience,
            'education_form':education_form,
            'experience_form':experience_form,
            'indentity_form':IdentityForm(instance=onboarding,company=company),
            'experience_form':experience_form,
            'levels' : levels,
            'courses' : courses,
            'specs' : specs,
            'years' : range(2000, 2030),
            'page':page,
            
        }
        return render(request,'jobseeker/onboarding.html',context)


    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
    




# API 
# for get job post beased on user input like keyword and location as p and q
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def ApiSearch(request):
    try:
        keyword1 = request.GET.get('q', '')
        keyword2 = request.GET.get('p', '')        
        page_number = request.GET.get('page', 2)
        if request.user.is_authenticated:
            candidate = Candidates.objects.get(user=request.user)
        else:
            candidate = False
        jobs = search_job(request,keyword1,keyword2,page_number,candidate)

        # Pagination
        paginator = Paginator(jobs, 10)  # Show 20 jobs per page
        page_obj = paginator.get_page(page_number)

        # Filter
        filters = get_filter_from_job(jobs)


        serializer = JobsCardSerializer(page_obj, many=True)
        api_response = {
            'jobs': serializer.data,  # Serialized job list
            'keyword1': keyword1,
            'keyword2': keyword2,
            'filters': filters,
            'pagination': {
                'page_from': page_obj.start_index(),
                'page_to': page_obj.end_index(),
                'page_of': page_obj.paginator.count,
                'total_pages': paginator.num_pages,
                'current_pages': page_obj.number,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        }
        return Response(api_response)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


# for get job post beased on user input like keyword and location as p and q
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def ApiTitle(request):
    try:
        title_query = Jobs.objects.values('title') \
            .annotate(job_count=Count('title')) \
            .order_by('-job_count')
            # .order_by('-job_count')[:50]

        locations_query = Locations.objects.annotate(
        job_count=Count('location_map_jlm')  # Reverse name from Jobs.location_id
            ).filter(job_count__gt=0).order_by('-job_count')

        
        data = {
            'titles': TitleSerializer(title_query, many=True).data,
            'locations': LocationSerializer(locations_query, many=True).data
        }
        
        return Response(data)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)




# HTMX
def HTMXOnboardingLanguages(request):
    candidate = Candidates.objects.get(user=request.user)
    if request.htmx:
        languages = UserLanguages.objects.filter(candidate=candidate)
        return render(request,"jobseeker/htmx/onboarding_language_show.html",context={'languages':languages,})
    else:
        return redirect("job_seeker:profile")

def HTMXOnProfileLanguages(request):
    candidate = Candidates.objects.get(user=request.user)
    if request.htmx:
        languages = UserLanguages.objects.filter(candidate=candidate)
        return render(request,"jobseeker/htmx/profileLanguageShow.html",context={'my_languages':languages,})
    else:
        return redirect("job_seeker:profile")


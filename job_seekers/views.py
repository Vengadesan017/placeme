from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Case, When, Q, CharField
from django.db.models.functions import Concat
from django.db.models import Value as V, F
from django.db import transaction
from django.core.paginator import Paginator
from django.core.files.storage import default_storage

from credentials.models import Users
from recruiters.models import Jobs , Locations, Qualifications , OfferLetters
from .models import Candidates, JobApplications, Onboarding, EducationMap , UserLanguages,\
    UserLocations, LevelForEdu, CourseForEdu, Skills, Employment, Internship, Bookmarks, \
        Familys, SpecificationForEdu ,EducationType 
from .forms import CandidatePersonalUpdateForm, CandidateEducationUpdateForm, OnboardingCandidatePersonalForm,\
        OnboardingPersonalForm ,CandidateLanguageUpdateForm, CandidateLocationUpdateForm, CandidateCareerUpdateForm,\
        CandidateEmploymentUpdateForm, CandidateIntenshipUpdateForm, OnboardingFamilyForm, \
        ResumeForm, ProfileForm
from .serializers import JobsCardSerializer, TitleSerializer, LocationSerializer
from .services import apply_filter_in_job,get_filter_from_job,search_job
from .decorators import is_onboarding

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




def Home(request):
    try:
        jobs_titles = Jobs.objects.values_list('title', flat=True) \
            .annotate(job_count=Count('title')) \
            .order_by('-job_count')[:5]
        # jobs_titles = Jobs.objects.values_list('title', flat=True).distinct()
        context = {
            'jobs_titles': jobs_titles,
        }
        return render(request,'jobseeker/home.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@login_required
def Profile(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        if request.method == 'POST':
            if 'profile_personal_edit' in request.POST:
                form = CandidatePersonalUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                    messages.info(request, 'Your profile has been updated successfully.')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')

            elif 'profile_education_create' in request.POST:
                form = CandidateEducationUpdateForm(request.POST)
                if form.is_valid():
                    form.save(candidate=candidate)
                    messages.info(request, 'Your New Education has been added successfully.')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data.')
            elif 'upload_resume' in request.POST:
                form = ResumeForm(request.POST, request.FILES, instance= candidate)
                if form.is_valid():
                    form.save(candidate=candidate, user = request.user)
                    messages.info(request, 'Your Resume Uploaded successfully')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data.')
            elif 'upload_profile' in request.POST:
                form = ProfileForm(request.POST, request.FILES,instance=candidate)
                if form.is_valid():
                    candidate = form.save(commit=False)

                    if 'profile_pic' in request.FILES:
                        # Delete old profile picture
                        if candidate.profile_pic and default_storage.exists(candidate.profile_pic.name):
                            default_storage.delete(candidate.profile_pic.name)

                        # Assign the new file
                        candidate.profile_pic = request.FILES['profile_pic']

                    candidate.save()
                    messages.success(request, "Profile picture updated successfully.")
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data.')

            elif 'SelectEducation' in request.POST:
                index = request.POST.get("SelectEducation")
                educationEdit = CandidateEducationUpdateForm(request.POST, instance=EducationMap.objects.filter(candidate=candidate)[index-1])
                # if form.is_valid():
                #     form.save()
                #     messages.info(request, 'Your profile has been updated successfully.')
                    
                # else:
                #     print("Form errors:", form.errors)
                #     messages.error(request, 'Please enter the valid data')
            elif 'profile_education_edit' in request.POST:
                form = CandidateEducationUpdateForm(request.POST, instance=EducationMap.objects.filter(candidate=candidate))
                if form.is_valid():
                    form.save()
                    messages.info(request, 'Your profile has been updated successfully.')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')


            elif 'profile_skill_edit' in request.POST:
                new_skill = request.POST.get('new_skill')  # Get new skill from the request
                if new_skill or new_skill.strip():
                    if candidate.add_skill(new_skill) :  # Use the method to add the skill
                        messages.info(request, 'Skill was successfully added')
                    else :
                        messages.warning(request, 'Already existing skill')
                        return redirect('job_seeker:profile')
                    
                else:
                    messages.error(request, 'No skills selected')

            elif 'profile_preference_edit' in request.POST:
                if request.POST.get('language_id'):
                    form = CandidateLanguageUpdateForm(request.POST)
                    if form.is_valid():
                        form.save(candidate=candidate)
                        messages.info(request, 'Language was successfully added.')

                    else:
                        print("Form errors:", form.errors)
                        messages.error(request, 'Please enter the valid data')

                if request.POST.get('location'):
                    form = CandidateLocationUpdateForm(request.POST)
                    if form.is_valid():
                        form.save(candidate=candidate)
                        messages.info(request, 'Location was successfully added.')

                    else:
                        print("Form errors:", form.errors)
                        messages.error(request, 'Please enter the valid data')
                        
            elif 'profile_employment_create' in request.POST:
                form = CandidateEmploymentUpdateForm(request.POST)
                if form.is_valid():
                    form.save(candidate=candidate)
                    messages.info(request, 'Your Education has been updated successfully.')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')

            elif 'profile_internship_create' in request.POST:
                form = CandidateIntenshipUpdateForm(request.POST)
                if form.is_valid():
                    form.save(candidate=candidate)
                    messages.info(request, 'Your Internship has been updated successfully.')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')

            elif 'profile_career_edit' in request.POST:
                form = CandidateCareerUpdateForm(request.POST, instance=candidate)
                if form.is_valid():
                    form.save()
                    messages.info(request, 'Your career data has been updated successfully.')
                    
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')

                    


        new_education = CandidateEducationUpdateForm()
        new_employment = CandidateEmploymentUpdateForm()
        new_internship = CandidateIntenshipUpdateForm()
        education = EducationMap.objects.filter(candidate=candidate)
        language = UserLanguages.objects.filter(candidate=candidate)
        location = UserLocations.objects.filter(candidate=candidate)
        employment = Employment.objects.filter(candidate=candidate)
        internship = Internship.objects.filter(candidate=candidate)
        new_language = CandidateLanguageUpdateForm()
        new_location = CandidateLocationUpdateForm()
        skills = Skills.objects.all()
        profile = ProfileForm()
        resume = ResumeForm()
        

        level = LevelForEdu.objects.all()
        course = CourseForEdu.objects.all()
        years = range(2000, 2030)


        skills_list = [skill.strip() for skill in candidate.skill.split(',')] if candidate.skill else []
        context = {
            'candidate': candidate,
            'skills_list': skills_list,
            'education': education,
            'employment': employment,
            'internship': internship,
            'new_education': new_education,
            'new_employment': new_employment,
            'new_internship': new_internship,
            'language': language,
            'location': location,
            'new_language': new_language,
            'new_location': new_location,
            'profile': profile,
            'resume':resume,
            'level':level,
            'course':course,
            'years' :years,
            'skills' : skills
            # 'doc':doc
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
        
        # # Apply filter
        # if request.method == "POST":
        #     if 'filter_jobs' in request.POST:
        #         jobs = apply_filter_in_job(request,jobs)

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
        job1 = request.GET.get('r', '')
        job = Jobs.objects.get(slug=job1)
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
                

        # skills_list = [skill.strip() for skill in job.skills.split(',')] if job.skills else []
        context = {
            'job': job,
            # 'skills_list':skills_list,
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
                # slug = request.POST.get('slug') 
                slug = request.POST.get('slug') 
                title = request.POST.get('title') 
                job = Jobs.objects.get(slug=slug)
                candidate = Candidates.objects.get(user=request.user)
                # user_id = candidate.user_id
                JobApplications.objects.create(
                    candidate=candidate,
                    job=job
                )
                # job = Jobs.objects.get(slug=slug)
                job.increment_applied_count()
                messages.info(request, f'You have successfully applied to {title} job')
                referer_url = request.META.get('HTTP_REFERER')
                if referer_url:
                    return redirect(referer_url)
                else:
                    return redirect('job_seeker:home')
                # return redirect('job_seeker:status', page="applied")
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
                    messages.info(request, f'Job unsaved successfully')
                    candidate.increment_bookmarks_count(False)
                elif candidate.bookmarks_count <15:
                    b = Bookmarks.objects.create(
                        candidate=candidate,
                        job=job
                    )
                    if b:
                        candidate.increment_bookmarks_count(True)
                        messages.info(request, f'Job saved successfully')
                    else:
                        messages.info(request, f'Not able to save the job')
                else :
                    messages.error(request, f'Job has not able to save. You reached your usage limit.')  


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
        applied_list = ['Applied' ,'Viewed' ,'Shortlisted' ,'Selected' ]
        offered_list = ['Selected', 'Offered', 'Accepted', 'Rejected' ,'Hired' ]
        job_status = False
        onboarding_id = False
        offer = False
        # if request.method == "POST":
        #     if "view_appiled_status" in request.POST:
        #         id = request.POST.get("id")
        #         job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()

        #     elif "view_offered_status" in request.POST:
        #         id = request.POST.get("id")
        #         job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()
        #         onboarding_id = Onboarding.objects.filter(candidate=candidate,job_post=job_status.id).values_list('Onbording_id').first()
        if page and id:
            if page == 'applied':
                job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()

            if page == 'offered' and job_status:
                onboarding_id = Onboarding.objects.filter(candidate=candidate,job_post=job_status.id).values_list('Onbording_id',flat=True).first()


        bookmarks = Bookmarks.objects.filter(candidate=candidate).values_list('job')
        jobs = Jobs.objects.filter(job_id__in=bookmarks)
        job_applications = JobApplications.objects.filter(candidate=candidate)
        applied = job_applications.filter(offered_at__isnull=True)
        offered = job_applications.filter(offered_at__isnull=False)


        if not job_status:
            if page == "applied":
                if applied.exists():
                    job_status = applied[0]
                    
            elif page == "offered":
                if offered.exists():
                    job_status = offered[0]
                    onboarding_id = Onboarding.objects.filter(candidate=candidate,job_post=job_status.id).values_list('Onbording_id').first()
                    id = job_status.id
        if not onboarding_id:
            onboarding_id = False
        else:
            onboarding_id = onboarding_id[0]

        # for offer letter
        if job_status:
            if page == 'offered' and job_status.offer_id :
                # offer = get_object_or_404(OfferLetters, offers_id=job_status.offer_id)

                # Mark as viewed if not yet
                if not job_status.offer_id.is_view:
                    job_status.offer_id.is_view = True
                    job_status.offer_id.viewed_at = timezone.now()
                    job_status.offer_id.save()

        if request.method == "POST":
            job_application_id = request.POST.get('application_id')
            offer_letter_id = request.POST.get('offer_id')
            response_message = request.POST.get('response', '')
            acknowledgment = request.POST.get('acknowledgment') == 'on'
            accept = 'accept' in request.POST
            decline = 'decline' in request.POST

            # Ensure both exist
            application = JobApplications.objects.filter(id=job_application_id, candidate=candidate).first()
            offer = OfferLetters.objects.filter(offers_id=offer_letter_id).first() if application else None

            if not application or not offer:
                messages.error(request, 'Application or Offer Letter not found.')
                return redirect('job_seeker:status', page='offered')

            if not acknowledgment:
                messages.error(request, 'You must acknowledge the terms and conditions.')
                return redirect('job_seeker:status', page='offered')

            try:
                with transaction.atomic():
                    # Update OfferLetter
                    offer.response = response_message
                    offer.is_acknowledged = True
                    if accept:
                        offer.approve_at = timezone.now()
                        offer.approve_by = request.user.candidate
                    else:
                        offer.approve_at = None
                        offer.approve_by = None
                    offer.save()

                    # Update JobApplications
                    if accept:
                        application.status = 'Accepted'
                        application.accepted_at = timezone.now()
                    elif decline:
                        application.status = 'Rejected'
                        application.rejected_at = timezone.now()
                    application.save()

                messages.success(request, "Your response has been recorded.")
                return redirect('job_seeker:status', page='offered')

            except Exception as e:
                messages.error(request, f"Something went wrong: {str(e)}")
                return redirect('job_seeker:status', page='offered')
        # if request.method == "POST":
        #     action = request.POST.get("action")
        #     if action == "accept" and not offer.is_accepted:
        #         offer.is_accepted = True
        #         offer.accepted_at = timezone.now()
        #         offer.save()
        #         messages.success(request, "You have accepted the offer.")
        #     elif action == "decline" and not offer.is_accepted:
        #         offer.is_accepted = False
        #         offer.accepted_at = None
        #         offer.save()
        #         messages.info(request, "You have declined the offer.")
        print("p=offer----",offer)
        context = {
            'bookmarks': jobs,
            'applied': applied,
            'offered': offered,
            'applied': applied,
            'job_status': job_status,
            'offer': offer,
            'onboarding_id':onboarding_id,
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
        if request.method == 'POST':
            if 'personal' in request.POST:
                    
                candidate_form = OnboardingCandidatePersonalForm(request.POST, request.FILES, instance=Candidates.objects.get(user=request.user))
                onboarding_form = OnboardingPersonalForm(request.POST, request.FILES, instance=Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id))
                if not candidate_form.is_valid():
                    messages.error(request, candidate_form.errors)
                else:
                    candidate_form.save()
                    # x(not cleaned_data.get(field) for field in ['firstname', 'lastname', 'dob', 'email']):
                if not onboarding_form.is_valid():
                    messages.error(request, onboarding_form.errors)
                    print(onboarding_form.errors)
                else:
                    onboarding_form.save()
                page = "family"


                # return render(request,'jobseeker/onboarding.html',context)
                # return render(request,'jobseeker/onboarding.html',context)

            if 'family' in request.POST:
                # Create a list to hold the form instances
                create_family_forms = []
                edit_family_forms = []
                

                # Get the data from the request
                id = request.POST.getlist('id[]')
                first_names = request.POST.getlist('txtFirstName[]')
                last_names = request.POST.getlist('txtLastName[]')
                genders = request.POST.getlist('Gender[]')
                relationships = request.POST.getlist('Releationship[]')
                aadhar_numbers = request.POST.getlist('txtAadhar[]')
                dob = request.POST.getlist('txtdob[]')
                mobile_numbers = request.POST.getlist('txtFContactNo[]')
                # Loop through the lists and create forms for each family member
                edit_family_original_forms =Familys.objects.filter(candidate=candidate)
                for i in range(len(first_names)):
                    if first_names[i] and last_names[i] and genders[i] and relationships[i]:
                        if id[i]:
                            family_edit = {
                                'first_name': first_names[i],
                                'last_name': last_names[i],
                                'gender': genders[i],
                                'relationship': relationships[i],
                                'dob':dob[i],
                                'aadhar_no': aadhar_numbers[i],
                                'mobile_no': mobile_numbers[i]
                            }
                            family_id= edit_family_original_forms.filter(family_member_id=id[i])
                            # Create and add the form to the list
                            edit_family_forms.append(OnboardingFamilyForm(family_edit, instance=family_id[0]))
                        else:
                            family_data = {
                                'first_name': first_names[i],
                                'last_name': last_names[i],
                                'gender': genders[i],
                                'relationship': relationships[i],
                                'dob':dob[i],
                                'aadhar_no': aadhar_numbers[i],
                                'mobile_no': mobile_numbers[i]
                            }
                            # Create and add the form to the list
                            create_family_forms.append(OnboardingFamilyForm(family_data))

                # # Validate and save each form if valid
                for form in create_family_forms:

                    if form.is_valid():
                        form.save(candidate=candidate)
                    else:
                        print("Form errors:", form.errors)
                        
                for form in edit_family_forms:

                    if form.is_valid():
                        form.save()
                    else:
                        print("Form errors:", form.errors)

                page = "education"
                    

                # return render(request,'jobseeker/onboarding.html',context)

        candidate_form = OnboardingCandidatePersonalForm(instance=Candidates.objects.get(user=request.user))
        # onboarding_form = OnboardingPersonalForm(instance=Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id))
        onboarding = Onboarding.objects.get(candidate=candidate,Onbording_id=onboarding_id)
        onboarding_form = OnboardingPersonalForm(instance=onboarding)
        company = 1
        print(onboarding)
        create_family_forms =Familys.objects.filter(candidate=candidate)

        context = {
            'company':company,
            'candidate': candidate_form,
            'onboarding': onboarding_form,
            'family_forms': create_family_forms,
            'onboarding_id':onboarding_id,
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




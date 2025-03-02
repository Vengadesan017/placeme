from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Candidates, JobApplications, Onboarding, EducationMap , UserLanguages, UserLocations, LevelForEdu, CourseForEdu, Skills, Employment, Internship, Bookmarks, Familys, SpecificationForEdu ,EducationType 
from recruiters.models import Jobs , Locations, Qualifications
from credentials.models import Users
from django.contrib.auth.decorators import login_required
from .forms import CandidatePersonalUpdateForm, CandidateEducationUpdateForm, OnboardingCandidatePersonalForm, OnboardingPersonalForm ,CandidateLanguageUpdateForm, CandidateLocationUpdateForm, CandidateCareerUpdateForm, CandidateEmploymentUpdateForm, CandidateIntenshipUpdateForm, OnboardingFamilyForm
from django.contrib import messages
from django.db.models import Count, Case, When, Q
from functools import wraps
from .services import apply_filter_in_job,get_filter_from_job,search_job
from .serializers import JobsCardSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

def is_onboarding(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        onboarding_id = kwargs.get("onboarding_id")
        candidate = Candidates.objects.filter(user=request.user).first()
        # print("1 ",candidate)
        if candidate:
            onboarding = Onboarding.objects.filter(candidate=candidate, Onbording_id=onboarding_id).first()
            # print("2 ",onboarding)
            if onboarding:
                if onboarding.created_date and not onboarding.completed_date and not onboarding.closed:
                    # print("3 ",onboarding)
                    return view_func(request, *args, **kwargs)
        messages.warning(request, "You do not have access to enter the onboarding page.")
        return redirect('job_seeker:home')
    return _wrapped_view

def Home(request):
    try:
        jobs_titles = Jobs.objects.values_list('title', flat=True).distinct()
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
        page_number = request.GET.get('page', 1)
        jobs = search_job(request,keyword1,keyword2,page_number)
        if not jobs:
            context = {
                'page_obj': False
            }
            return render(request, 'jobseeker/jobs.html', context)
        
        # Apply filter
        if request.method == "POST":
            if 'filter_jobs' in request.POST:
                jobs = apply_filter_in_job(request,jobs)

        # Bookmaked jobs
        if request.user.is_authenticated:
            candidate = Candidates.objects.get(user=request.user)
            bookmarked_job_ids = Bookmarks.objects.filter(candidate=candidate).values_list('job_id', flat=True)
            bookmarks = jobs.filter(job_id__in=bookmarked_job_ids)
            
            applied_job_ids = JobApplications.objects.filter(candidate=candidate).values_list('job_id',flat=True)
            applied = jobs.filter(job_id__in=applied_job_ids)
        else:
            bookmarks = False  
            applied = False  

        # Pagination
        paginator = Paginator(jobs, 10)  # Show 20 jobs per page
        page_obj = paginator.get_page(page_number)

        # Filter
        filters = get_filter_from_job(jobs)

        context = {
            'page_obj': page_obj,
            'keyword1': keyword1,
            'keyword2': keyword2,
            'filters' : filters,
            'bookmarks' : bookmarks,
            'applied' : applied
        }
        return render(request, 'jobseeker/jobs.html', context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def ApiSearch(request):
    job_title = request.GET.get('q', '')
    location = request.GET.get('location', '')

    jobs = Jobs.objects.all()
    
    if job_title:
        jobs = jobs.filter(title__icontains=job_title)
    
    if location:
        jobs = jobs.filter(location__location__icontains=location)
    
    serializer = JobsCardSerializer(jobs, many=True)
    return Response(serializer.data)

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
                

        skills_list = [skill.strip() for skill in job.skills.split(',')] if job.skills else []
        context = {
            'job': job,
            'skills_list':skills_list,
            'applied': applied,
            'login':login
        }
        return render(request,'jobseeker/job.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def MyJob(request):
    return HttpResponse("<h1>You applied jobs are shown here</h1>")

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
                elif candidate.bookmarks_count <15:
                    b = Bookmarks.objects.create(
                        candidate=candidate,
                        job=job
                    )
                    if b:
                        candidate.increment_bookmarks_count()
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
def Status(request, page):
    try:
        candidate=Candidates.objects.get(user=request.user)
        applied_list = ['Applied' ,'Viewed' ,'Shortlisted' ,'Selected' ]
        offered_list = ['Selected', 'Offered', 'Accepted', 'Rejected' ,'Hired' ]
        job_status = False
        onboarding_id = False
        if request.method == "POST":
            if "view_appiled_status" in request.POST:
                id = request.POST.get("id")
                job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()

            elif "view_offered_status" in request.POST:
                id = request.POST.get("id")
                job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()
                onboarding_id = Onboarding.objects.filter(candidate=candidate,job_post=job_status.id).values_list('Onbording_id').first()



        bookmarks = Bookmarks.objects.filter(candidate=candidate).values_list('job')
        jobs = Jobs.objects.filter(job_id__in=bookmarks)
        job_applications = JobApplications.objects.filter(candidate=candidate)
        applied = job_applications.filter(status__in=applied_list)
        offered = job_applications.filter(status__in=offered_list)


        if not job_status:
            if page == "applied":
                if applied.exists():
                    job_status = applied[0]
                    
            elif page == "offered":
                if offered.exists():
                    job_status = offered[0]
                    onboarding_id = Onboarding.objects.filter(candidate=candidate,job_post=job_status.id).values_list('Onbording_id').first()
        if not onboarding_id:
            onboarding_id = False
        else:
            onboarding_id = onboarding_id[0]
        print(onboarding_id)
        context = {
            'bookmarks': jobs,
            'applied': applied,
            'offered': offered,
            'applied': applied,
            'job_status': job_status,
            'onboarding_id':onboarding_id,
            'page': page, 
        }
        return render(request,'jobseeker/status.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


def Notifications(request):
    return HttpResponse("<h1>Notifications are With pop up window</h1>")

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
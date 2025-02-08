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
        # keyword='web'
        # page_number=1

        # Basic keyword search
        if keyword1 and keyword2:
            # jobs = Jobs.objects.filter(title__icontains=keyword1, location__icontains=keyword2)
            jobs = Jobs.objects.filter(
                title__icontains=keyword1,
                location_id__location__icontains=keyword2  # Filtering based on the location field
            )
            if not jobs.exists():
                jobs = Jobs.objects.filter(title__icontains=keyword1)

            jobs = jobs.order_by('job_id')
            
        elif keyword1:
            jobs = Jobs.objects.filter(title__icontains=keyword1)
            jobs = jobs.order_by('job_id')
        else :
            context = {
                'search': 'Search your dream job'
           }
            return render(request, 'jobseeker/jobs.html', context)
        message = 'Search your dream job.'

        if request.method == "POST":
            if 'filter_jobs' in request.POST:
                selected_work_modes = request.POST.getlist('work_mode')  
                experience = request.POST.get('experience') 
                salary = request.POST.getlist('salary')  
                organization = request.POST.getlist('organization')  
                employment_type = request.POST.getlist('employment_type')  
                qualification = request.POST.getlist('qualification')  
                industry_type = request.POST.getlist('industry_type')  
                location = request.POST.getlist('location')  
                query = Q()
                if selected_work_modes:
                    # Add conditions dynamically based on selected work modes
                    if 'On site' in selected_work_modes:
                        query &= Q(is_onsite=True)  # Use AND condition
                    if 'Hybrid' in selected_work_modes:
                        query &= Q(is_hybrid=True)
                    if 'Work From Home' in selected_work_modes:
                        query &= Q(is_work_from_home=True)
                    jobs = jobs.filter(query)
                if int(experience) >= 0:
                    jobs = jobs.filter(min_experience__lte=experience, max_experience__gte=experience)
                if salary:
                    salary_ranges = {
                        "0_3_LPA": (0, 300000),
                        "3_6_LPA": (300000, 6),
                        "6_10_LPA": (600000, 1000000),
                        "10_15_LPA": (1000000, 1500000),
                        "15_25_LPA": (1500000, 2500000),
                        "25_plus_LPA": (2500000, None),  
                    }

                    # Normalize and transform the user-selected salary keys
                    salary = {
                        key.replace("+", "_plus").replace(" LPA", "_LPA").replace("-", "_")
                        for key in salary
                    }
                    

                    query = Q()
                    for key in salary:
                        if key in salary_ranges:
                            start, end = salary_ranges[key]
                            if end is not None:
                                query |= Q(salary__gte=start, salary__lt=end)
                            else:
                                query |= Q(salary__gte=start)  
                    jobs = jobs.filter(query)
                if organization:
                    jobs = jobs.filter(company__organization_type__in=organization)
                if employment_type:
                    jobs = jobs.filter(employment_type__in=employment_type)
                if qualification:
                    jobs = jobs.filter(qualifications__qualification__in=qualification)
                if industry_type:
                    jobs = jobs.filter(company__industry_type__in=industry_type)
                if location:
                    jobs = jobs.filter(location_id__location__in=location)
                jobs = jobs.distinct()
        if request.user.is_authenticated:
            candidate = Candidates.objects.get(user=request.user)
            bookmarked_job_ids = Bookmarks.objects.filter(candidate=candidate).values_list('job_id', flat=True)
            bookmarks = jobs.filter(job_id__in=bookmarked_job_ids)
        else:
            bookmarks = False  

        # Pagination
        paginator = Paginator(jobs, 10)  # Show 20 jobs per page
        page_obj = paginator.get_page(page_number)





        # Filter
        location_counts = jobs.filter(qualifications__isnull=False).values('location_id__location').annotate(count=Count('job_id', distinct=True))
        location_data = {}
        for item in location_counts:
            location_data[item['location_id__location']] = location_data.get(item['location_id__location'], 0) + item['count']

        employment_type_counts = jobs.values('employment_type').annotate(count=Count('job_id'))
        employment_type_data = {}
        for item in employment_type_counts:
            employment_type_data[item['employment_type']] = employment_type_data.get(item['employment_type'], 0) + item['count']

        experience_counts = jobs.values('min_experience').annotate(count=Count('job_id'))
        experience_data = {}
        for item in experience_counts:
            experience_data[item['min_experience']] = experience_data.get(item['min_experience'], 0) + item['count']

        shift_counts = {
            'is_fixed_shift': jobs.filter(is_fixed_shift=True).count(),
            'is_rotational_shift': jobs.filter(is_rotational_shift=True).count(),
        }

        fixed_shift_counts = {
            'is_day_shift': jobs.filter(is_day_shift=True).count(),
            'is_night_shift': jobs.filter(is_night_shift=True).count(),
        }

        work_mode_counts = {
            'On site': jobs.filter(is_onsite=True).count(),
            'Work From Home': jobs.filter(is_work_from_home=True).count(),
            'Hybrid': jobs.filter(is_hybrid=True).count(),
        }

        salary_ranges = {
            '0_3_LPA': Count(Case(When(salary__gte=0, salary__lt=3_00_000, then=1))),
            '3_6_LPA': Count(Case(When(salary__gte=3_00_000, salary__lt=6_00_000, then=1))),
            '6_10_LPA': Count(Case(When(salary__gte=6_00_000, salary__lt=10_00_000, then=1))),
            '10_15_LPA': Count(Case(When(salary__gte=10_00_000, salary__lt=15_00_000, then=1))),
            '15_25_LPA': Count(Case(When(salary__gte=15_00_000, salary__lt=25_00_000, then=1))),
            '25_plus_LPA': Count(Case(When(salary__gte=25_00_000, then=1))),
        }
        salary_counts = jobs.aggregate(**salary_ranges)

        salary_counts = {
            key.replace("_plus","+").replace("_LPA", " LPA").replace("_", "-"): value
            for key, value in salary_counts.items()
        }

        qualification_data = qualification_counts = jobs.filter(qualifications__isnull=False).values('qualifications__qualification').annotate(count=Count('job_id', distinct=True))
        qualification_counts = {}
        for item in qualification_data:
            qualification_counts[item['qualifications__qualification']] = qualification_counts.get(item['qualifications__qualification'], 0) + item['count']

        industry_counts = jobs.values('company__industry_type').annotate(count=Count('job_id'))
        industry_data = {item['company__industry_type']: item['count'] for item in industry_counts if item['company__industry_type']}

        organization_counts = jobs.values('company__organization_type').annotate(count=Count('job_id'))
        organization_data = {item['company__organization_type']: item['count'] for item in organization_counts if item['company__organization_type']}

        filters = {
            'location':  location_data,
            'employment_type':  employment_type_data,
            'work_mode':  work_mode_counts,
            'shift':  shift_counts,
            'fixed_shift':  fixed_shift_counts,
            'salary':  salary_counts,
            'experience':  experience_data,
            'industry_type':  industry_data,
            'organization_type':  organization_data,
            'qualification':  qualification_counts,
        }
        context = {
            'page_obj': page_obj,
            'keyword1': keyword1,
            'keyword2': keyword2,
            'filters' : filters,
            'bookmarks' : bookmarks
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
        if request.method == "POST":
            if "view_appiled_status" in request.POST:
                id = request.POST.get("id")
                job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()

            elif "view_offered_status" in request.POST:
                id = request.POST.get("id")
                job_status = JobApplications.objects.filter(id=id,candidate=candidate).first()



        bookmarks = Bookmarks.objects.filter(candidate=candidate).values_list('job')
        jobs = Jobs.objects.filter(job_id__in=bookmarks)
        applied = JobApplications.objects.filter(candidate=candidate, status__in=applied_list)
        offered = JobApplications.objects.filter(candidate=candidate,status__in=offered_list)

        if not job_status:
            if page == "applied":
                if applied.exists():
                    job_status = applied[0]
            elif page == "offered":
                if offered.exists():
                    job_status = offered[0]

        context = {
            'bookmarks': jobs,
            'applied': applied,
            'offered': offered,
            'applied': applied,
            'job_status': job_status,
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
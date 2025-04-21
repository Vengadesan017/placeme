from .models import Jobs, JobApplications, Bookmarks
# from recruiters.models import Jobs
# from .serializers import JobSerializer
from django.db.models import Count, Case, When, Q
from django.db.models import OuterRef, Exists
from django.contrib import messages

def search_job(request,keyword1=None,keyword2=None,page_number=None,candidate=None):

    if candidate:
        # Get user bookamrks and saved applications
        job_application_exists = JobApplications.objects.filter(
            candidate=candidate,
            job=OuterRef('pk')
        )
        bookmarks_exists = Bookmarks.objects.filter(
            candidate=candidate,
            job=OuterRef('pk')
        )
        # Basic keyword search with annotation
        if keyword1 and keyword2:
            # jobs = Jobs.objects.filter(title__icontains=keyword1, location__icontains=keyword2)
            jobs = Jobs.objects.annotate(
            is_applied=Exists(job_application_exists),
            is_saved=Exists(bookmarks_exists)
            ).filter(
                title__icontains=keyword1,
                location_id__location__icontains=keyword2  # Filtering based on the location field
            )
            if not jobs.exists():
                messages.warning(request, "No job vacancy matches your desired location")
                jobs = Jobs.objects.annotate(
                    is_applied=Exists(job_application_exists),
                    is_saved=Exists(bookmarks_exists)
                ).filter(
                    title__icontains=keyword1
                )        
        elif keyword1:
            jobs = Jobs.objects.annotate(
                is_applied=Exists(job_application_exists),
                is_saved=Exists(bookmarks_exists)
            ).filter(
                title__icontains=keyword1
            )
        else :
            return False

    else :
        # Basic keyword search without annotation
        if keyword1 and keyword2:
            # jobs = Jobs.objects.filter(title__icontains=keyword1, location__icontains=keyword2)
            jobs = Jobs.objects.filter(
                title__icontains=keyword1,
                location_id__location__icontains=keyword2  # Filtering based on the location field
            )
            if not jobs.exists():
                messages.warning(request, "No job vacancy matches your desired location")
                jobs = Jobs.objects.filter(title__icontains=keyword1)        
        elif keyword1:
            jobs = Jobs.objects.filter(title__icontains=keyword1)
        else :
            return False

    if jobs.exists():
        # ORDER THE JOB POST
        jobs = jobs.order_by('-posted_date')
    else:
        messages.error(request, "No Job found.. ")
    
    return jobs


def apply_filter_in_job(request,jobs):
    """ Apply the filter in jobs variable"""
    
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
    
    return jobs


def get_filter_from_job(jobs):
    """ Get the filter from jobs variable"""
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
    
    return filters
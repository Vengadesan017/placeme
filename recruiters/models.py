from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
# from django.contrib.auth import get_user_model
import hashlib
import datetime
from django.utils.text import slugify
from credentials.models import Users
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
# from job_seekers.models import Candidates

from django.db import transaction
from django.db.models import Max

EXPERIENCE_CHOICES = [
    (0, "Fresher"),
    (1, "1 year"),
    (2, "2 years"),
    (3, "3 years"),
    (5, "5 years"),
    (7, "7 years"),
    (10, "10 years"),
    (15, "15 years"),
    (20, "20 years"),
    (25, "25 years"),
    (30, "30 years"),
    (30, "35 years"),
    (30, "40+ years"),
]


def path_by_user_id(user_id: int):
    user_id_int = user_id + 100000000
    revchar = ''
    i=1
    while user_id_int>0:
        rem = user_id_int%10
        revchar += chr(rem+48)
        user_id_int //= 10
        if (i == 3 or i == 6):
            revchar += '/'
        i +=1       
    path = revchar[::-1] 
    return path


def validate_file_size(file):
    max_size = 1024 * 1024 * 5 # 5 MB limit
    if file.size > max_size:
        raise ValidationError("File size must be under 200KB.")

def upload_company_kyc_doc(instance, filename):
    Company_path = path_by_user_id(instance.company_id)    
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'CompaniesDF/{0}/kyc/{1}'.format(Company_path,filename)

def upload_offerleters(instance, filename):
    Company_path = path_by_user_id(instance.company_id)    
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'CompaniesDF/{0}/offer_letters/{1}'.format(Company_path,filename)


class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    candidate = models.OneToOneField('job_seekers.Candidates', on_delete=models.CASCADE, related_name='company_candidate', null=True, blank=True)
    company_name = models.CharField(max_length=150)
    state = models.CharField(max_length=255,blank=True,null=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    permanent_address = models.CharField(max_length=255)
    communication_address = models.CharField(max_length=255)
    official_email  = models.EmailField(validators=[EmailValidator()])
    contact_no = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    admin_name = models.CharField(max_length=255)
    admin_role = models.CharField(max_length=255)
    Company_type  = models.CharField(max_length=100, choices=[
        ('Limited liability', 'Limited liability'),
        ('Sole proprietorship', 'Sole proprietorship'),
        ('Partnership', 'Partnership'),
        ('Private limited', 'Private limited'),
        ('Public limited', 'Public limited') ,
        ('Non-profit', 'Non-Profit'),
        ('Government', 'Government')
    ], blank=True, null=True)
    no_of_employees = models.CharField(max_length=20,blank=True,null=True)
    on_role_employees = models.CharField(max_length=20,blank=True,null=True)
    off_role_employees = models.CharField(max_length=20,blank=True,null=True)
    business_type = models.CharField(max_length=100, choices=[
        ('Manufacturing', 'Manufacturing'),
        ('Service', 'Service')        
    ], blank=True, null=True)
    industry_type  = models.CharField(max_length=100, blank=True, null=True)
    organization_type  = models.CharField(max_length=100, choices=[
        ('Start-Up', 'Start-Up'),
        ('Small and Medium-sized enterprises ', 'SME'),      
        ('Multinational-Corporation', 'MNC')
    ], blank=True, null=True)
    website = models.URLField(max_length=255,blank=True, null=True)
    linkedin = models.URLField(max_length=355,blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    established_at = models.IntegerField(blank=True,null=True)
    gst_no = models.CharField(max_length=255,blank=True,null=True)
    pan_no = models.CharField(max_length=255,blank=True,null=True)
    back_ifsc_no = models.CharField(max_length=255,blank=True,null=True)
    profile_pic = models.FileField(upload_to=upload_company_kyc_doc, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    gst_doc = models.FileField(upload_to=upload_company_kyc_doc, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            validate_file_size
        ]
    )
    pan_doc = models.FileField(upload_to=upload_company_kyc_doc, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            validate_file_size
        ]
    )
    list_of_dir_doc = models.FileField(upload_to=upload_company_kyc_doc, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            validate_file_size
        ]
    )
    bank_account_doc = models.FileField(upload_to=upload_company_kyc_doc, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            validate_file_size
        ]
    )
 
    sub_users_limit = models.IntegerField(default=1)
    is_email_verified = models.BooleanField(default=False)
    is_contact_verified = models.BooleanField(default=False)
    is_kyc_verified = models.BooleanField(default=False)
    kyc_uploaded_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class Jobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='jobs',blank=True,null=True)
    title = models.CharField(max_length=255)
    location_id = models.ManyToManyField('recruiters.Locations', related_name='location_map_jlm')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    benefit_id = models.ManyToManyField('recruiters.Benefits', related_name='benefit_map_jbm')    
    employment_type  = models.CharField(max_length=100, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Fixed-term', 'Fixed-term'),
        ('Internship', 'Internship') 

    ], blank=True, null=True)
    is_fixed_shift = models.BooleanField(default=False)
    is_rotational_shift = models.BooleanField(default=False)
    is_day_shift = models.BooleanField(default=False)
    is_night_shift = models.BooleanField(default=False)
    is_onsite = models.BooleanField(default=False)
    is_work_from_home = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    skills = models.ManyToManyField('job_seekers.Skills', related_name='job_post_skills', blank=True)
    qualifications = models.ManyToManyField('job_seekers.SpecificationForEdu', related_name='qualification_map')
    hire_request = models.ForeignKey('recruiters.HireRequests', related_name='job_post_hire_request',on_delete=models.PROTECT, blank=True, null=True)
    min_experience = models.IntegerField(
        choices=EXPERIENCE_CHOICES,
        blank=True,
        null=True
    )
    max_experience = models.IntegerField(
        choices=EXPERIENCE_CHOICES,
        blank=True,
        null=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_type  = models.CharField(max_length=10, choices=[
        ('CTC', 'CTC'),
        ('Take home', 'Take home'),
        ('Per year', 'Per year'),
        ('Per month', 'Per month'),
        ('Per hour', 'Per hour') 

    ],default='CTC', blank=True, null=True)
    posted_date = models.DateTimeField(default=timezone.now)
    refreshed_date = models.DateTimeField(default=timezone.now)
    last_date_to_apply = models.DateTimeField(blank=True, null=True)
    opening_count = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(default=0)
    applied_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='create_job_post', null=True, blank=True)  
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_post_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            company_slug = self.company.company_name
            # x
            base_slug = slugify(f"{self.title} {company_slug}")
            
            now = datetime.datetime.now() 
            timestamp = now.strftime("%Y%m%d%H%M%S%f")
            # timestamp = str(int(time.time()))
            # unique_string = f"{self.title}-{self.location}-{company_slug}-{timestamp}"
            unique_string = f"{self.title}-{company_slug}-{timestamp}"
            unique_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:8]
            
            slug = f"{base_slug}-{unique_hash}"
            
            while Jobs.objects.filter(slug=slug).exists():
                unique_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:8]
                slug = f"{slug}-{unique_hash}"
            
            self.slug = slug
        
        super(Jobs, self).save(*args, **kwargs)

    def increment_applied_count(self):
        self.applied_count += 1
        self.save()
        
    def days_since_posted(self):
        # Calculate the days between posted_date and now
        difference = timezone.now() - self.posted_date
        return difference.days

    def __str__(self):
        return self.title


class OfferLetters(models.Model):
    offers_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='company_offer', null=True, blank=True)
    application = models.ForeignKey('job_seekers.JobApplications', on_delete=models.CASCADE, related_name='application_offer', null=True, blank=True)
    offer_letter = models.FileField(upload_to=upload_offerleters, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_file_size
        ]
    )
    is_view = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(blank=True,null=True)
    is_acknowledged = models.BooleanField(default=False)
    response = models.CharField(max_length=255,blank=True,null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='generate_offer', null=True, blank=True)
    approve_at = models.DateTimeField(blank=True,null=True)
    approve_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='approve_offer', null=True, blank=True)    

    def __str__(self):
        return f"{self.company} - {self.offer_letter}"


# class SubUserAccess(models.Model):
#     subuser_access_id = models.AutoField(primary_key=True)
#     company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='subusers_company', null=True, blank=True)
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subuser_access', null=True, blank=True)
#     can_post_jobs = models.BooleanField(default=False)
#     can_edit_jobs = models.BooleanField(default=False)
#     can_view_applicants = models.BooleanField(default=False)


#     def __str__(self):
#         return f"{self.user.email} - {self.company.company_name} Access"


class BookmarkCandidates(models.Model): # change all the column
    bookmark_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='job_seekers_bookmarks', null=True, blank=True)
    job = models.ForeignKey('recruiters.Jobs', on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.email} bookmarked {self.job.title}"


class Commands(models.Model):
    command_id = models.AutoField(primary_key=True)
    issued_company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='command_from', null=True, blank=True)
    issued_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='command_by', null=True, blank=True) 
    issued_to = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='command_for', null=True, blank=True)
    job = models.ForeignKey('recruiters.Jobs', on_delete=models.CASCADE, related_name='command_in')
    command = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"Command issued by {self.issued_by.firstname} {self.issued_by.lastname}to {self.issued_to.user.email}"


class UserLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    sub_user = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE,related_name='subusers_logs',blank=True, null=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)




# =====================================Location begin========================================================

class CountryForLoc(models.Model):
    country_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class StateForLoc(models.Model):
    state_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100)
    country = models.ForeignKey(CountryForLoc, related_name="states", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class DistrictForLoc(models.Model):
    district_id = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100)
    state = models.ForeignKey(StateForLoc, related_name="districts", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.state.name and self.state.country.name:
            return f"{self.name}, {self.state.name}, {self.state.country.name}"
        elif self.state.name:
            return f"{self.name}- {self.state.name}"
        else :
            return f"{self.name}"

class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    pincode = models.IntegerField(null=True, blank=True)
    district = models.ForeignKey(DistrictForLoc, related_name="locations", on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey('job_seekers.Candidates', related_name='location_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        if self.district:
            if self.location.lower()==self.district.name.lower():
                return f'{self.location}' 
            else:
                return f'{self.location} - {self.district.name}'
        else:
            return f'{self.location}' 
            
    @property
    def display_name(self):
        return str(self)
# =====================================Location End========================================================
# =====================================Benefits begin========================================================
class Benefits(models.Model):
    benefits_id = models.AutoField(primary_key=True)
    benefit = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    Created_by = models.ForeignKey('job_seekers.Candidates',on_delete=models.CASCADE, related_name='benefit_by',null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.benefit

# class JobsBenefitsMaps(models.Model):
#     jobs_benefits_id = models.AutoField(primary_key=True)
#     job_id = models.ManyToManyField('recruiters.Jobs', related_name='job_map_jbm')
#     benefit_id = models.ManyToManyField('recruiters.Benefits', related_name='benefit_map_jbm')

#     def __str__(self):
#         jobs = ', '.join([job_id.slug for job_id in self.job_id.all()])
#         return f'Jobs: {jobs}'
# =====================================Benefits End========================================================
# =====================================Job Role title Begin========================================================


class JobTitle(models.Model):
    job_title_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=200)
    created_by = models.ForeignKey('job_seekers.Candidates', related_name='job_title_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)   

    def __str__(self):
        return f"{self.title} by {self.created_by}"
    
# class JobTitle(models.Model):
#     jobtitle_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

# =====================================Job Role title End========================================================
# =====================================Job Qualifications Begin========================================================


class Qualifications(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=200)
    created_by = models.ForeignKey('job_seekers.Candidates', related_name='job_qualification_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)   

    def __str__(self):
        return f"{self.qualification}"
    
# =====================================Job Qualifications End========================================================
# =====================================Position Manager Begin========================================================


class Positions(models.Model):
    position_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=255)
    position_code = models.PositiveIntegerField(blank=True,null=True) 
    # status  = models.CharField(max_length=100, choices=[  # need to change
    #     ('Full-time', 'Hiring-Needed'),
    #     ('Open', 'Open'),
    #     ('Close', 'Close')

    # ], blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    remarks = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='create_position', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    upadted_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='update_position', null=True, blank=True)    
    deadline = models.DateTimeField(blank=True,null=True)   # not needed
    is_open = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('company', 'position_code')  # Ensures no duplicate serial numbers for each company

    def __str__(self):
        return f"{self.position_title} - {self.position_code}"

    def save(self, *args, **kwargs):
        if not self.position_code:
            # Use a transaction to ensure atomic operation and prevent race conditions
            with transaction.atomic():
                # # Find the maximum serial_number for the company and increment by 1
                # last_position = PositionManager.objects.filter(company=self.company).aggregate(Max('position_code'))
                # max_serial_number = last_position['position_code__max']
                last_position = Positions.objects.filter(company=self.company).order_by('-position_code').values_list('position_code', flat=True).first()
                self.position_code = last_position + 1 if last_position else 1001
                
                # Save the new PositionManager instance
                super(Positions, self).save(*args, **kwargs)

        else:
            super(Positions, self).save(*args, **kwargs)

class HireRequests(models.Model):
    hire_request_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    hire_request_code = models.PositiveIntegerField(blank=True,null=True)  # generate and validate
    # status  = models.CharField(max_length=100, choices=[  # need to change
    #     ('Open', 'Open'),
    #     ('Close', 'Close')

    # ], blank=True, null=True)
    employee_id = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='employee_in_hirerequest', null=True, blank=True)
    hire_date = models.DateTimeField(null=True, blank=True)
    leave_date = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='create_hire_request', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    upadted_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='update_hire_request', null=True, blank=True)    
    deadline = models.DateTimeField(blank=True,null=True)
    is_open = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('company', 'hire_request_code')

    def __str__(self):
        return f"{self.position.position_title} - {self.hire_request_code}"
        return f"{self.hire_request_code} - {self.position.position_title} ({self.company.company_name})"

    def save(self, *args, **kwargs):
        if not self.hire_request_code:
            # Use a transaction to ensure atomic operation and prevent race conditions
            with transaction.atomic():
                # # Find the maximum serial_number for the company and increment by 1
                # last_position = PositionManager.objects.filter(company=self.company).aggregate(Max('hire_request_code'))
                # max_serial_number = last_position['hire_request_code__max']
                # last_position = PositionManager.objects.filter(company=self.company).order_by('-serial_number').values_list('').first()
                # self.hire_request_code = max_serial_number + 1 if max_serial_number else 1
                last_position = HireRequests.objects.filter(company=self.company).order_by('-hire_request_code').values_list('hire_request_code', flat=True).first()
                self.hire_request_code = last_position + 1 if last_position else 5001
                self.is_open= True
                
                # Save the new PositionManager instance
                super(HireRequests, self).save(*args, **kwargs)

        else:
            super(HireRequests, self).save(*args, **kwargs)



class EmployeePositionManager(models.Model):  # not needed merge to hire request
    employee_position_id = models.AutoField(primary_key=True)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    hire_request = models.ForeignKey(HireRequests, on_delete=models.CASCADE,blank=True,null=True)
    employee_id = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='employee_in_position_manager', null=True, blank=True)
    hire_date = models.DateTimeField(null=True, blank=True)
    leave_date = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='map_position', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    upadted_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='update_map_position', null=True, blank=True)    
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return f"{self.position} ({self.employee_id})"


# =====================================Position Manager End========================================================
# =====================================Admin Control Begin========================================================
class SubUsers(models.Model):
    subuser_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companies, on_delete=models.PROTECT, related_name='recruiters_company', null=True, blank=True) 
    user = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='recruiters_subuser', null=True, blank=True) 
    is_recruiter = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_payroll_maker = models.BooleanField(default=False)
    is_payroll_checker = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='create_subusers', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    upadted_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='update_subuser', null=True, blank=True)    
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.company} ({self.user.user.email})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding  
        super().save(*args, **kwargs)  # First, save the SubUser
        if is_new and self.user:
            try:

                credentials_user = self.user.user
                credentials_user.is_recruiter = True
                credentials_user.save()
            except AttributeError:
                pass  # Or log an error if relation doesn't exist
                print(f"Error at give recuiter access to {self.user.user.email}")


# =====================================Admin Control End========================================================



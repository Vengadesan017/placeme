from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
import hashlib
import datetime
from django.utils.text import slugify
from credentials.models import Users
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
# from job_seekers.model import Candidates

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
    max_size = 200 * 1024  # 200KB limit
    if file.size > max_size:
        raise ValidationError("File size must be under 200KB.")

def upload_company_kyc_doc(instance, filename):
    Company_path = path_by_user_id(instance.company_id)    
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'CompaniesDF/{0}/kyc/{1}'.format(Company_path,filename)


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
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
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
    skills = models.TextField( null=True, blank=True)
    qualifications = models.ManyToManyField('recruiters.Qualifications', related_name='qualification_map')
    min_experience = models.IntegerField(blank=True, null=True)
    max_experience = models.IntegerField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_date = models.DateTimeField(default=timezone.now)
    last_date_to_apply = models.DateTimeField(blank=True, null=True)
    opening_count = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(default=0)
    applied_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
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


class SubUserAccess(models.Model):
    subuser_access_id = models.AutoField(primary_key=True)
    company = models.ForeignKey('recruiters.Companies', on_delete=models.CASCADE, related_name='subusers_company', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subuser_access', null=True, blank=True)
    can_post_jobs = models.BooleanField(default=False)
    can_edit_jobs = models.BooleanField(default=False)
    can_view_applicants = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.email} - {self.company.company_name} Access"


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
    sub_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='subusers_logs',blank=True, null=True)
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
        return f"{self.name}, {self.state.name}, {self.state.country.name}"

class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    pincode = models.IntegerField(null=True, blank=True)
    district = models.ForeignKey(DistrictForLoc, related_name="locations", on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(Users, related_name='location_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        if self.location.lower()==self.district.name.lower():
            return f'{self.location}'
        else:
            return f'{self.location} - {self.district.name}'

# =====================================Location End========================================================
# =====================================Benefits begin========================================================
class Benefits(models.Model):
    benefits_id = models.AutoField(primary_key=True)
    benefit = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    Created_by = models.ForeignKey(Users,on_delete=models.CASCADE, related_name='benefit_by',null=True,blank=True)
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
# =====================================Job Role title End========================================================


class JobTitle(models.Model):
    job_title_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=200)
    created_by = models.ForeignKey(Users, related_name='job_title_by', on_delete=models.CASCADE, null=True, blank=True)
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
# =====================================Job Qualifications End========================================================


class Qualifications(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=200)
    created_by = models.ForeignKey(Users, related_name='job_qualification_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)   

    def __str__(self):
        return f"{self.qualification}"
    
# =====================================Job Qualifications End========================================================
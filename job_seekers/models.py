from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from credentials.models import Users  # Import the custom Users model
# from .models import Candidates
from recruiters.models import Jobs,OfferLetters # Import the Jobs model from recruiters app
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

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



# def validate_file_type(file):
#     mime = magic.from_buffer(file.read(1024), mime=True)
#     valid_mime_types = ['application/pdf', 'image/png', 'image/jpeg']    
#     if mime not in valid_mime_types:
#         raise ValidationError("Invalid file type.")
#     file.seek(0)

def validate_file_size(file):
    max_size = 1024 * 1024  # 1MB limit
    if file.size > max_size:
        raise ValidationError("File size must be under 200KB.")

def upload_profile_pic(instance, filename):
    user = getattr(instance, 'user', None)
    if user and hasattr(user, 'userid'):
        user_path = path_by_user_id(user.userid)
    else:
        user_path = 'unknown_user'
    # user_path = path_by_user_id(instance.user.userid)    
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'UsersDF/{0}/personal/Profile_{1}'.format(user_path,filename)

def upload_profile_resume(instance, filename):
    user_path = path_by_user_id(instance.user.userid)
    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'UsersDF/{0}/personal/Resume_{1}'.format(user_path,filename)

def upload_onboarding(instance, filename):
    user_path = path_by_user_id(instance.candidate.user.userid)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    # Generate path based on email and timestamp
    # return 'UsersDF/{0}/personal/Profile_Pic_{1}_{2}'.format(user_path(),timestamp,filename)
    return 'UsersDF/{0}/onboarding/{2}_{1}'.format(user_path,filename,timestamp)

class Candidates(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='candidate', null=True, blank=True)
    
    # Personal Information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    work_status = models.CharField(max_length=15, choices=[('Fresher', 'Fresher'), ('Experienced', 'Experienced')], blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    linkedin_profile = models.URLField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.IntegerField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married')], blank=True, null=True)
    last_update = models.DateField(default=now)   
    profile_pic = models.FileField(upload_to=upload_profile_pic, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    resume = models.FileField(upload_to=upload_profile_resume, null=True, blank=True, validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            validate_file_size
        ]
    )
    
    # # Education Information
    # highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    # specialization = models.CharField(max_length=100, blank=True, null=True)
    # year_of_graduation = models.IntegerField(blank=True, null=True)
    # university_name = models.CharField(max_length=255, blank=True, null=True)
    # secondary_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # higher_secondary_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # diploma_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # bachelors_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # masters_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    # doctorate_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    
    # Work Experience
    present_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    present_take_home = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_take_home = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    other_yearly_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    monthly_incentive = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    skill = models.TextField(blank=True, null=True)
    present_designation = models.CharField(max_length=200, blank=True, null=True)
    work_experience = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notice_period = models.IntegerField(null=True,blank=True)
    is_rotate_shift = models.BooleanField(default=False)
    preferred_location = models.CharField(max_length=100, blank=True, null=True)
    is_relocate = models.BooleanField(default=False)
    professional_summary = models.TextField(blank=True, null=True)

    # Additional info
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    email_otp_count = models.IntegerField(default=3)
    phone_otp_count = models.IntegerField(default=3)
    bookmarks_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Update the field with the current date on every save
        self.date_field = now().date()
        super().save(*args, **kwargs)

    def add_skill(self, new_skill):
        """
        Add a new skill to the existing skills. If the skill already exists, do nothing.
        """
        if self.skill:
            skill_list = [skill.strip() for skill in self.skill.split(',')]  # Split existing skills
            if new_skill not in skill_list:
                skill_list.append(new_skill)  # Append new skill
                self.skill = ', '.join(skill_list)  # Join updated skills
            else :
                return False
        else:
            self.skill = new_skill  # Add the first skill

        self.save()     
        return True   
    def increment_bookmarks_count(self,increase):
        if increase:
            self.bookmarks_count += 1
        else:
            self.bookmarks_count -= 1
        self.save()
    def __str__(self):
        return f'{self.first_name}'

# class Documents(models.Model):
#     document_id = models.AutoField(primary_key=True)
#     candidate = models.OneToOneField('Candidates', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
#     profile_picture = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
#     resume = models.BinaryField(blank=True, null=True, validators=[validate_file_size, validate_file_type])
    
#     def __str__(self):
#         return f'{self.candidate.user.email} - {self.profile_picture}'

class Bookmarks(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='bookmarks', null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='user_bookmarks',null=True,blank=True)
    bookmarked_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.candidate.user.email} - {self.job}'


# =====================================Onboarding begin========================================================

class Onboarding(models.Model):
    Onbording_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='onbording_candidate', null=True, blank=True)
    job_post = models.ForeignKey('JobApplications', on_delete=models.CASCADE,related_name='onboarding_job',null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    mobile_two = models.BigIntegerField(null=True,blank=True)
    communication_country = models.CharField(max_length=100, blank=True, null=True)
    communication_state = models.CharField(max_length=100, blank=True, null=True)
    communication_city = models.CharField(max_length=100, blank=True, null=True)
    communication_address = models.CharField(max_length=255, blank=True, null=True)
    communication_pincode = models.IntegerField(null=True, blank=True)    
    doj = models.DateField(null=True,blank=True)
    dol = models.DateField(null=True,blank=True)

    # Educational Documents
    photo = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),validate_file_size])

    # Personal Documents
    aadhar_card = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),validate_file_size])
    bank_book = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),validate_file_size])
    pf = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),validate_file_size])
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='onbording_verified_by', null=True, blank=True)
    opened_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='onbording_opened_by', null=True, blank=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.candidate.user.email} - {self.aadhar_card}'

class Familys(models.Model):
    family_member_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='user_family', null=True, blank=True)
    job_post = models.ForeignKey('JobApplications', on_delete=models.CASCADE,related_name='onboarding_family_job',null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True,blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=[('Male','Male'),('Female','Female'),('Transgender','Transgender'),('NotDisclosed','NotDisclosed')])
    relationship = models.CharField(max_length=50, choices=[
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Spouse', 'Spouse'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister')
    ])
    aadhar_no = models.BigIntegerField(null=True,blank=True)
    mobile_no = models.BigIntegerField( null=True,blank=True)

    def __str__(self):
        return f"{self.candidate.first_name} {self.relationship}"


# =====================================Onboarding end========================================================
class JobApplications(models.Model):
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='candidate_form', null=True, blank=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='job_applications', null=True, blank=True)  
    offer_id = models.ForeignKey(OfferLetters, on_delete=models.CASCADE, related_name='job_applications_offer', null=True, blank=True)  
    status = models.CharField(max_length=50, choices=[
        ('Viewed', 'Viewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Interviewed', 'Interviewed'),
        ('Selected', 'Selected'),
        ('Offered', 'Offered'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired')
    ], default='Applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(blank=True, null=True)    
    not_shortlisted_at = models.DateTimeField(blank=True, null=True)    
    shortlisted_at = models.DateTimeField(blank=True, null=True)    
    interview_at = models.DateTimeField(blank=True, null=True)    
    selected_at = models.DateTimeField(blank=True, null=True)    
    offered_at = models.DateTimeField(blank=True, null=True)    
    accepted_at = models.DateTimeField(blank=True, null=True)    
    onboarding_at = models.DateTimeField(blank=True, null=True)    
    rejected_at = models.DateTimeField(blank=True, null=True)    
    hired_at = models.DateTimeField(blank=True, null=True)    
    viewed_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='viewed_by', null=True, blank=True)
    shortlisted_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='shortlisted_by', null=True, blank=True)
    interview_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='interview_by', null=True, blank=True)
    selected_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='viewselected_byed_by', null=True, blank=True)
    offered_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='offered_by', null=True, blank=True)
    onboarded_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='onboarded_by', null=True, blank=True)
    hired_by = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='hired_by', null=True, blank=True)
    
    def __str__(self):
        return f'{self.candidate.user.email} - {self.status}'

class AdditionalInfo(models.Model):
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='candidate_info', null=True, blank=True)
    # job_post_info = models.ForeignKey('Jobs', on_delete=models.CASCADE, related_name='job_post_info')      <=======================> uncommand <=-=-=-=-=-=-=--=-=-=-=->
    post = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='postinfo', null=True, blank=True)   
    info_name = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.candidate.user.email} - {self.info_name}'

# =====================================Skills begin========================================================

class DomainForSkill(models.Model):
    domain_id = models.AutoField(primary_key=True)     
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)     
    domain = models.ForeignKey(DomainForSkill, related_name="skills", on_delete=models.CASCADE, null=True, blank=True)
    skill = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Candidates, related_name='Skill_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)    

    def __str__(self):
        if self.domain:
            return f"{self.skill} ({self.domain.name})"
        else :
            return f"{self.skill}"

# =====================================Skills End========================================================
# =====================================Education begin========================================================

class LevelForEdu(models.Model):
    level_id = models.AutoField(primary_key=True)     
    name = models.CharField(max_length=50, unique=True)  # Example: "Undergraduate" or "Postgraduate" 
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Example: "UB" or "PB"

    def __str__(self):
        return f"{self.code} - {self.name}"

class CourseForEdu(models.Model):
    course_id = models.AutoField(primary_key=True)
    level = models.ForeignKey(LevelForEdu, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)  # Example: "Bachelor of Technology" | degree | B.Tech


    def __str__(self):
        return f"{self.name}"

class SpecificationForEdu(models.Model):
    specification_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(CourseForEdu, related_name="specialities", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)  # Example: "Computer Science and Engineering", "Information Technology"
    created_by = models.ForeignKey(Candidates, related_name='education_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        if self.course:
            if self.course.name.lower()==self.name.lower():
                return f'{self.name}' 
            else:
                return f"{self.course} {self.name}"
        else:
            return f'{self.name}' 


class EducationType(models.Model):
    edu_type_id = models.AutoField(primary_key=True)
    edu_type = models.CharField(max_length=50)  # Example: "Full-time" or "Part-time"


    def __str__(self):
        return f"{self.edu_type}"

# =====================================Education End========================================================
# =====================================Language Begin========================================================
class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=100)
    created_by = models.ForeignKey(Candidates, related_name='language_by', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)    

    def __str__(self):
        return f"{self.language}"
    
class UserLanguages(models.Model):
    user_language_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='user_language', null=True, blank=True)
    language_id = models.ForeignKey(Languages, related_name="language_user", on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_speak = models.BooleanField(default=False)
    proficiency = models.CharField(max_length=50, choices=[
        ('Proficient', 'Proficient'),
        ('Advanced', 'Advanced'),
        ('Intermediate', 'Intermediate'),
        ('Beginner', 'Beginner')
    ],null=True,blank=True)

    def __str__(self):
        return f"{self.candidate.first_name} Knows {self.language_id.language}"


# =====================================Language End========================================================
# =====================================workCompany Begin========================================================

class Employment(models.Model):
    work_company_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='employment_company', null=True, blank=True)
    company_name = models.CharField(max_length=200)
    company_role = models.CharField(max_length=200)
    doj = models.DateField(null=True,blank=True)
    dol = models.DateField(null=True, blank=True)
    reason_for_leaving = models.TextField(null=True,blank=True)
    type_id = models.ForeignKey('EducationType',on_delete=models.CASCADE, related_name='emp_type',null=True,blank=True)
    doc = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),validate_file_size])
    
    def __str__(self):
        return f"{self.candidate.first_name} worked in {self.company_name}"
    
class Internship(models.Model):
    internship_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='internship_company', null=True, blank=True)
    company_name = models.CharField(max_length=200)
    company_role = models.CharField(max_length=200)
    doj = models.DateField(null=True,blank=True)
    dol = models.DateField(null=True, blank=True)
    what_did = models.TextField(null=True,blank=True)
    doc = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),validate_file_size])

    
    def __str__(self):
        return f"{self.candidate.first_name} worked in {self.company_name}"

# =====================================workCompany End========================================================
# =====================================EducationName map begin========================================================

class EducationMap(models.Model):
    edu_map_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='candidate_to_edu_map', null=True, blank=True)
    edu_id = models.ForeignKey('SpecificationForEdu',on_delete=models.CASCADE, related_name='edu_to_user_map',null=True,blank=True)
    institute = models.CharField(max_length=200, null=True, blank=True)
    year_of_passing = models.IntegerField(null=True,blank=True)
    score = models.CharField(max_length=20,null=True,blank=True)
    type_id = models.ForeignKey('EducationType',on_delete=models.CASCADE, related_name='edu_type_map',null=True,blank=True)
    doc = models.FileField(upload_to=upload_onboarding, blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'Pdf']),validate_file_size])


    def __str__(self):
        if self.candidate.first_name and self.edu_id:
            return f'{self.candidate.first_name} - {self.edu_id}'

        else:
            return f'{self.edu_map_id}'


# =====================================EducationName Map End========================================================
# =====================================Locations begin========================================================

class UserLocations(models.Model):
    user_location_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey('Candidates', on_delete=models.CASCADE, related_name='user_location', null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.location}"

# =====================================Locations End========================================================
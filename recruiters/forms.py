from django.utils.timezone import now
from django import forms
from recruiters.models import Locations , Companies, Jobs, Positions,\
    HireRequests, Benefits, PositionGroup
from job_seekers.models import Skills, SpecificationForEdu
from django.db.models import Count
from job_seekers.forms import CommaDecimalField

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['candidate', 'company_name', 'permanent_address', 'communication_address', 'state','city','official_email',
                  'contact_no', 'phone_no', 'admin_name', 'admin_role', 'Company_type', 'no_of_employees',
                  'on_role_employees', 'off_role_employees','business_type', 'industry_type', 'organization_type',
                  'website', 'linkedin', 'about', 'established_at']

        labels = {
            'candidate': 'Candidate',
            'company_name': 'Company name',
            'permanent_address': 'Permanent address',
            'communication_address': 'Communication address',
            'state': 'State',
            'city': 'City',
            'official_email': 'Official email',
            'contact_no': 'Contact number',
            'phone_no': 'Phone number',
            'admin_name': 'Administrator name',
            'admin_role': 'Administrator role',
            'Company_type': 'Company type',
            'no_of_employees': 'Total number of employees',
            'on_role_employees': 'On-roll employees',
            'off_role_employees': 'Off-roll employees',
            'business_type': 'Business type',
            'industry_type': 'Industry type',
            'organization_type': 'Organization type',
            'website': 'Company website',
            'linkedin': 'LinkedIn profile',
            'about': 'About the company',
            'established_at': 'Year established',
        }

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance
    
class CreateCompanyKYCForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['gst_no', 'gst_doc', 'pan_no', 'pan_doc', 'back_ifsc_no',
                  'bank_account_doc', 'list_of_dir_doc']
        
        labels = {
            'gst_no': 'GST number',
            'gst_doc': 'GST document',
            'pan_no': 'PAN number',
            'pan_doc': 'PAN document',
            'back_ifsc_no': 'Bank IFSC number',
            'bank_account_doc': 'Bank account document',
            'list_of_dir_doc': 'List of directors document',
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.kyc_uploaded_at = now()
        if commit:
            instance.save()
        return instance

    
class CreateJobs(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = [
             'company', 'title', 'location_id', 'slug', 'description', 'benefit_id',
            'employment_type', 'is_fixed_shift', 'is_rotational_shift', 'is_day_shift',
            'is_night_shift', 'is_onsite', 'is_work_from_home', 'is_hybrid', 'skills',
            'qualifications', 'min_experience', 'max_experience', 'salary','salary_type',
            'last_date_to_apply', 'opening_count', 'hire_request', 'position_grp'
        ]
        labels = {
            'hire_request': 'Hire request',
            'position_grp': 'Position',
            'company': 'Company',
            'title': 'Job title',
            'location_id': 'Job location',
            'slug': 'Job slug (URL identifier)',
            'description': 'Job description',
            'benefit_id': 'Job benefits',
            'employment_type': 'Employment type',
            'is_fixed_shift': 'Fixed shift',
            'is_rotational_shift': 'Rotational shift',
            'is_day_shift': 'Day shift',
            'is_night_shift': 'Night shift',
            'is_onsite': 'On-site',
            'is_work_from_home': 'Work from home',
            'is_hybrid': 'Hybrid work',
            'skills': 'Required skills',
            'qualifications': 'Qualifications',
            'min_experience': 'Minimum experience (in years)',
            'max_experience': 'Maximum experience (in years)',
            'salary': 'Salary',
            'salary_type': 'Salary type (e.g. Monthly, Yearly)',
            'last_date_to_apply': 'Last date to apply',
            'opening_count': 'Number of openings',
        }

        widgets = {
            'salary_type': forms.Select(attrs={
                'class': 'admin-input-sel',
                # 'style': 'width: 35%;',
            }),
            'position_grp': forms.Select(attrs={
                'class': 'admin-input-sel',
            }),
            'hire_request': forms.Select(attrs={
                'class': 'admin-input-sel',
            }),
            'min_experience': forms.Select(attrs={
                'class': 'admin-input-sel'
            }),
            'max_experience': forms.Select(attrs={
                'class': 'admin-input-sel'
            }),
            'employment_type': forms.Select(attrs={
                'class': 'admin-input-sel'
            }),
            # 'qualifications': forms.Select(attrs={
            #     'class': 'company-input',
            #     'id': 'multi-select-qualifications',
            #     'style': 'display: none;',
            # }),
            # 'skills': forms.Select(attrs={
            #     'class': 'company-input',
            #     'id': 'multi-select-skills',
            #     'style': 'display: none;',
            # }),
        }
        
    salary = CommaDecimalField(required=False, max_digits=10, decimal_places=2) 
    def __init__(self, *args, position_group_id=None, **kwargs):
        
        company = kwargs.pop('company', None) 
        super().__init__(*args, **kwargs)
        
        if company:
            self.fields['position_grp'].queryset = PositionGroup.objects.filter(company=company, is_active=True)
            if position_group_id:
                self.fields['hire_request'].queryset = HireRequests.objects.filter(company=company, position_group = position_group_id, is_open=True, is_active=True)
            else:
                self.fields['hire_request'].queryset = HireRequests.objects.filter(company=company, is_open=True, is_active=True)

        my_hire_request = list(self.fields['hire_request'].choices)
        my_position_grp = list(self.fields['position_grp'].choices)
        
        self.fields['salary_type'].choices = [
            ('', 'Select the salary type...')
        ] + [choice for choice in self.fields['salary_type'].choices if choice[0] != '']

        self.fields['min_experience'].choices = [
            ('', 'Min Experience')
        ] + [choice for choice in self.fields['min_experience'].choices if choice[0] != '']

        self.fields['max_experience'].choices = [
            ('', 'Max Experience')
        ] + [choice for choice in self.fields['max_experience'].choices if choice[0] != '']

        self.fields['employment_type'].choices = [
            ('', 'Select Job Type')
        ] + [choice for choice in self.fields['employment_type'].choices if choice[0] != '']

        self.fields['hire_request'].choices = [
            ('', 'Select the Hire Request...')
        ] +[
            ('', 'Anonymous job Posting (Without hire request)')
        ] + [choice for choice in my_hire_request if choice[0] != '']

        self.fields['position_grp'].choices = [
            ('', 'Select the Position')
        ] +[
            ('', 'Anonymous job Posting (Without Position)')
        ] + [choice for choice in my_position_grp if choice[0] != '']

        # # return only 10 frequntly used posts
        # self.fields['location_id'].queryset = Locations.objects.annotate(
        #     job_count=Count('location_map_jlm')
        # ).order_by('-job_count')[:10]

        # self.fields['skills'].queryset = Skills.objects.annotate(
        #     job_count=Count('job_post_skills')
        # ).order_by('-job_count')[:10]

        # self.fields['qualifications'].queryset = SpecificationForEdu.objects.annotate(
        #     job_count=Count('qualification_map')
        # ).order_by('-job_count')[:10]

        # self.fields['benefit_id'].queryset = Benefits.objects.annotate(
        #     job_count=Count('benefit_map_jbm')
        # ).order_by('-job_count')[:10]

    
    def save(self, commit=True, company=None,created_by=None):
        instance = super().save(commit=False)
        if company:
            instance.company = company
        if created_by:
            instance.created_by = created_by
        if commit:
            instance.save()
        return instance
    
class PositionGroupForm(forms.ModelForm):
    class Meta:
        model = PositionGroup
        fields = [
            # 'company',
            'position_code',
            'position_title',
            'jd',
            'budget',
            'budget_type',
            'department',
            'cost_center',
            'locations',
            'Supervisor',
            'hrbp',
            'hrms',
            'division',
            'updated_by',
        ]
        labels = {
            # 'company': 'Company',
            'position_code': 'Position Code',
            'position_title': 'Position Title',
            'jd': 'Job Description',
            'budget': 'Budget',
            'budget_type': 'Budget Type',
            'department': 'Department',
            'cost_center': 'Cost Center',
            'locations': 'Locations',
            'Supervisor': 'Supervisor',
            'hrbp': 'HR Business Partner',
            'hrms': 'HRMS',
            'division': 'Division',
            'updated_by': 'updated_by',
        }


        
    def save(self, commit=True, company=None,created_by=None):
        instance = super().save(commit=False)
        if company:
            instance.company = company
        if created_by:
            instance.created_by = created_by
        if commit:
            instance.save()
        return instance
    budget = CommaDecimalField(required=False, max_digits=10, decimal_places=2)    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position_code'].disabled = True

class CreatePosition(forms.ModelForm):
    class Meta:
        model = Positions
        fields = [ 'remarks']
        labels = {
            'position': 'Position',
            # 'description': 'Description',
            'remarks': 'Remarks',
        }


        
    def save(self, commit=True, company=None,created_by=None):
        instance = super().save(commit=False)
        if company:
            instance.company = company
        if created_by:
            instance.created_by = created_by
        if commit:
            instance.save()
        return instance
    
class CreateHireRequest(forms.ModelForm):
    class Meta:
        model = HireRequests
        fields = [ 'position', 'hire_request_code', 'employee_id', 'hire_request_code',
                  'hire_date', 'leave_date', 'remarks', 'deadline', 'updated_by']

        labels = {
            'position': 'Position',
            'hire_request_code': 'Hire request code',
            'employee_id': 'Candidate',
            'hire_date': 'Hire date',
            'leave_date': 'Leave date',
            'remarks': 'Remarks',
            'deadline': 'Application deadline',
            'is_open': 'Is position open',
            'is_active': 'Is position active',
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        # self.fields['employee_id'].disabled = True
        self.fields['hire_request_code'].disabled = True
        self.fields['hire_date'].disabled = True
        self.fields['hire_date'].disabled = True
        # If company is passed, filter positions based on that company
        if company:
            self.fields['position'].queryset = Positions.objects.filter(
                company=company, is_open=True, is_active=True
            ).exclude(
                position_id__in=HireRequests.objects.filter(company=company).values('position_id')
            )

    def save(self, commit=True, company=None,created_by=None):
        instance = super().save(commit=False)
        if company:
            instance.company = company
        if created_by:
            instance.created_by = created_by
        if commit:
            instance.is_active = True
            instance.save()
        return instance
from django.utils.timezone import now
from django import forms
from recruiters.models import Locations , Companies, Jobs, Positions, HireRequests

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['candidate', 'company_name', 'permanent_address', 'communication_address', 'state','city','official_email',
                  'contact_no', 'phone_no', 'admin_name', 'admin_role', 'Company_type', 'no_of_employees',
                  'on_role_employees', 'off_role_employees','business_type', 'industry_type', 'organization_type',
                  'website', 'linkedin', 'about', 'established_at']
        
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
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.kyc_uploaded_at = now()
        if commit:
            instance.save()
        return instance
# class JobForm(forms.ModelForm):
#     locations = forms.ModelMultipleChoiceField(
#         queryset=Locations.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )


    # class Meta:
    #     model = Job
    #     fields = ['job_title', 'locations'] 
    
class CreateJobs(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = [
            'hire_request', 'company', 'title', 'location_id', 'slug', 'description', 'benefit_id',
            'employment_type', 'is_fixed_shift', 'is_rotational_shift', 'is_day_shift',
            'is_night_shift', 'is_onsite', 'is_work_from_home', 'is_hybrid', 'skills',
            'qualifications', 'min_experience', 'max_experience', 'salary','salary_type',
            'last_date_to_apply', 'opening_count'
        ]
        widgets = {
            'salary_type': forms.Select(attrs={
                'class': 'admin-input-sel',
                'style': 'width: 15%;',
            }),
            'hire_request': forms.Select(attrs={
                'class': 'admin-input-sel',
            }),
            # 'location_id': forms.Select(attrs={
            #     'class': 'company-input',
            #     'id': 'multi-select-location',
            #     'style': 'display: none;',
            # }),
            # 'benefit_id': forms.Select(attrs={
            #     'class': 'company-input',
            #     'id': 'multi-select-benefits',
            #     'style': 'display: none;',
            # }),
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
        
        
    def __init__(self, *args, **kwargs):
        
        company = kwargs.pop('company', None) 
        super().__init__(*args, **kwargs)
        
        if company:
            self.fields['hire_request'].queryset = HireRequests.objects.filter(company=company, is_open=True, is_active=True)

        my_hire_request = list(self.fields['hire_request'].choices)
        
        self.fields['salary_type'].choices = [
            ('', 'Select the salary type...')
        ] + [choice for choice in self.fields['salary_type'].choices if choice[0] != '']

        self.fields['hire_request'].choices = [
            ('', 'Select the Hire Request...')
        ] +[
            ('', 'Anonymous job Posting (Without hire request)')
        ] + [choice for choice in my_hire_request if choice[0] != '']

    
    def save(self, commit=True, company=None,created_by=None):
        instance = super().save(commit=False)
        if company:
            instance.company = company
        if created_by:
            instance.created_by = created_by
        if commit:
            instance.save()
        return instance
    
class CreatePosition(forms.ModelForm):
    class Meta:
        model = Positions
        fields = ['position_title', 'description', 'remarks']
        
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
        fields = [ 'position', 'hire_request_code', 'employee_id', 
                  'hire_date', 'leave_date', 'remarks', 'deadline', 'is_open', 'is_active']

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

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
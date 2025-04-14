from django.utils.timezone import now
from django import forms
from recruiters.models import Locations , Companies, Positions, HireRequests

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
            instance.save()
        return instance
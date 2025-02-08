from django.utils.timezone import now
from django import forms
from recruiters.models import Locations , Companies

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['candidate', 'company_name', 'permanent_address', 'communication_address', 'official_email',
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
    
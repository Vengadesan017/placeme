from django import forms
from .models import Candidates, Onboarding, EducationMap, UserLanguages, UserLocations, Employment, Internship, Familys


class CandidatePersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'linkedin_profile', 'country', 'state', 'city',
            'marital_status','languages','work_status'
        ]

class CandidateEducationUpdateForm(forms.ModelForm):
    class Meta:
        model = EducationMap
        fields = [
             'edu_id', 'institute', 'year_of_passing', 'score', 'type_id', 'doc'
        ]

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance

class OnboardingCandidatePersonalForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'marital_status', 
            'country', 'state', 'city', 'languages', 'address', 'pincode', 
            'linkedin_profile', 'profile_pic', 'resume'
        ]
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        #     'gender': forms.Select(attrs={'class': 'form-control'}),
        #     'dob': forms.DateInput(attrs={'class': 'form-control datetimepicker', 'type': 'date'}),
        #     'marital_status': forms.Select(attrs={'class': 'form-control'}),
        #     'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        #     'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        #     'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        #     'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Languages'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        #     'pincode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        #     'linkedin_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn Profile'}),
        #     'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        # }

class OnboardingPersonalForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = [
            'father_name', 'mobile_two', 'communication_country', 'communication_state', 
            'communication_city', 'communication_address', 'communication_pincode', 
            'doj', 'dol'
        ]
        # widgets = {
        #     'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
        #     'mobile_two': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mobile No 2'}),
        #     'communication_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        #     'communication_state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        #     'communication_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        #     'communication_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        #     'communication_pincode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        #     'doj': forms.DateInput(attrs={'class': 'form-control datetimepicker', 'type': 'date'}),
        #     'dol': forms.DateInput(attrs={'class': 'form-control datetimepicker', 'type': 'date'}),
        #     'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'aadhar_card': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'bank_book': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'pf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        # }

class OnboardingFamilyForm(forms.ModelForm):
    class Meta:
        model = Familys
        fields = ['first_name', 'last_name', 'gender', 'dob', 'relationship', 'aadhar_no', 'mobile_no']
        
    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance    

class CandidateLanguageUpdateForm(forms.ModelForm):
    class Meta:
        model = UserLanguages
        fields = [
             'language_id', 'can_read', 'can_write', 'can_speak', 'proficiency'
        ]

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance
    
class CandidateLocationUpdateForm(forms.ModelForm):
    class Meta:
        model = UserLocations
        fields = [
             'location'
        ]

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance

class CandidateCareerUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'present_ctc', 'present_take_home', 'expected_ctc', 'expected_take_home', 'notice_period', 'work_experience'
        ]


class CandidateEmploymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = [
             'company_name', 'company_role', 'doj', 'dol', 'type_id','reason_for_leaving', 'doc'
        ]

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance        
    
class CandidateIntenshipUpdateForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
             'company_name', 'company_role', 'doj', 'dol','what_did', 'doc'
        ]

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance        
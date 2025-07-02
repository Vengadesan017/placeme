from django import forms
from .models import Candidates, Onboarding, EducationMap, UserLanguages,\
    Employment, Internship, Familys,OnboardingDocumentRequirement,\
        SpecificationForEdu, OfferLetters
import datetime


class CandidatePersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'linkedin_profile', 'country', 'state', 'city',
            'marital_status','work_status'
        ]
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'gender': 'Gender',
            'dob': 'Date of birth',
            'linkedin_profile': 'LinkedIn profile',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'marital_status': 'Marital status',
            'work_status': 'Current work status',
        }
class CandidateSummaryUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'professional_summary'
        ]
        labels = {
            'professional_summary': 'Professional Summary',
        }
class CandidateSkillUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'skill'
        ]
        labels = {
            'skill': 'Key Skills',
        }


class CandidateEducationUpdateForm(forms.ModelForm):
    class Meta:
        model = EducationMap
        fields = [
             'edu_id', 'institute', 'year_of_passing','year_of_joining', 'currently', 'score', 'type_id', 'doc'
        ]
        labels = {
            'edu_id': 'Education level',
            'institute': 'Institute name',
            'year_of_joining': 'Year of joining',
            'year_of_passing': 'Year of passing',
            'currently': 'Currently',
            'score': 'Score / Grade',
            'type_id': 'Education type',
            'doc': 'Supporting document',
        }


    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        edu_obj = self.instance.edu_id  # This is the SpecificationForEdu object if editing

        self.fields['edu_id'].queryset = SpecificationForEdu.objects.select_related('course__level')

        # Extra hidden fields to use in the template (JS)
        self.level_id = None
        self.course_id = None

        if edu_obj:
            course = edu_obj.course
            level = course.level if course else None

            self.course_id = course.course_id if course else None
            self.level_id = level.level_id if level else None
            
            
class OnboardingCandidatePersonalForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'marital_status', 
            'country', 'state', 'city', 'address', 'pincode', 
            'linkedin_profile', 'profile_pic', 'resume'
        ]
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'gender': 'Gender',
            'dob': 'Date of birth',
            'marital_status': 'Marital status',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'address': 'Address',
            'pincode': 'Pincode',
            'linkedin_profile': 'LinkedIn profile',
            'profile_pic': 'Profile picture',
            'resume': 'Resume',
        }
        # error_messages = {
        #     'first_name': {
        #         'required': "First name is required.",
        #         'max_length': "First name can be at most 255 characters."
        #     }
        # }
    # def clean(self):
    #     cleaned_data = super().clean()  # Get cleaned data from Django
    #     required_fields = ['first_name', 'last_name', 'gender', 'dob', 'country', 'state', 'pincode']

    #     for field in required_fields:
    #         if not cleaned_data.get(field):
    #             self.add_error(None, f"{field.replace('_', ' ').capitalize()} is required.")
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
        
        labels = {
            'father_name': "Father's name",
            'mobile_two': 'Alternate mobile number',
            'communication_country': 'Communication country',
            'communication_state': 'Communication state',
            'communication_city': 'Communication city',
            'communication_address': 'Communication address',
            'communication_pincode': 'Communication pincode',
            'doj': 'Date of joining',
            'dol': 'Date of leaving',
        }


    
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
        

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'gender': 'Gender',
            'dob': 'Date of birth',
            'relationship': 'Relationship',
            'aadhar_no': 'Aadhar number',
            'mobile_no': 'Mobile number',
        }


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
        labels = {
            'language_id': 'Language',
            'can_read': 'Can read',
            'can_write': 'Can write',
            'can_speak': 'Can speak',
            'proficiency': 'Overall proficiency',
        }

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance
    
class CandidateLocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
             'preferred_location'
        ]
        labels = {
            'preferred_location': 'PreferedLocation',
        }



class CommaDecimalField(forms.DecimalField):
    def clean(self, value):
        if isinstance(value, str):
            value = value.replace(',', '')
        return super().clean(value)
class CandidateCareerUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'present_ctc_amount',
            'present_take_home_amount',
            'expected_ctc_amount',
            'expected_take_home_amount',
            'present_ctc_type',
            'present_take_home_type',
            'expected_ctc_type',
            'expected_take_home_type',
            'notice_period',
            'notice_period_negotiable',
            'work_experience_years',
            'work_experience_months',
        ]

        labels = {
            'present_ctc_amount': 'Present CTC (Cost to Company) amount',
            'present_take_home_amount': 'Present take-home salary amount',
            'expected_ctc_amount': 'Expected CTC amount',
            'expected_take_home_amount': 'Expected take-home salary amount',
            'present_ctc_type': 'Present CTC (Cost to Company) type',
            'present_take_home_type': 'Present take-home salary type',
            'expected_ctc_type': 'Expected CTC type',
            'expected_take_home_type': 'Expected take-home salary type',
            'notice_period': 'Notice period',
            'notice_period_negotiable': 'Negotiable Notice period',
            'work_experience_years': 'Work experience years',
            'work_experience_months': 'Work experience months',
        }
    # Override specific fields using custom field
    present_ctc_amount = CommaDecimalField(required=False, max_digits=10, decimal_places=2)
    present_take_home_amount = CommaDecimalField(required=False, max_digits=10, decimal_places=2)
    expected_ctc_amount = CommaDecimalField(required=False, max_digits=10, decimal_places=2)
    expected_take_home_amount = CommaDecimalField(required=False, max_digits=10, decimal_places=2)

class CandidateEmploymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = [
            'company_name',
            'company_role',
            'doj',
            'dol',
            'currently',
            'type_id',
            'reason_for_leaving',
            'doc',
            
        ]

        labels = {
            'company_name': 'Company name',
            'company_role': 'Role/Designation',
            'doj': 'Date of joining',
            'dol': 'Date of leaving',
            'currently': 'Currently',
            'type_id': 'Employment type',
            'reason_for_leaving': 'Reason for leaving',
            'doc': 'Relieving/Experience document',
        }
    doj = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m'],  # accepts only year and month
        required=False
    )
    dol = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m'],
        required=False
    )

    def clean_doj(self):
        doj = self.cleaned_data.get('doj')
        return datetime.date(doj.year, doj.month, 1) if doj else None

    def clean_dol(self):
        dol = self.cleaned_data.get('dol')
        return datetime.date(dol.year, dol.month, 1) if dol else None
    
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
        labels = {
        'company_name': 'Company name',
        'company_role': 'Role/Designation',
        'doj': 'Date of joining',
        'dol': 'Date of leaving',
        'what_did': 'Key responsibilities / What you did',
        'doc': 'Supporting document',
        }   

    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance        
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = ['profile_pic']
        
        labels = {
            'profile_pic': 'Profile Photo',
        }

    # def save(self, commit=True, candidate=None, user=None):
    #     instance = super().save(commit=False)
    #     if user and not instance.user:
    #         instance.user = user
    #     if commit:
    #         instance.save()
    #     return instance

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = ['resume']
        labels = {
            'resume': 'Resume',
        }
    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance
    


class IdentityForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = [
            'aadhar_number', 'aadhar_card',
            'pf_number', 'pf',
            'pan_number', 'pan_card',
            'bank_name', 'ifsc_code', 'account_number',
            'bank_book', 'pf_uan', 'esic_number',
            'address_proof',
        ]

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        # Make all fields not required by default + add form-control
        for field_name, field in self.fields.items():
            field.required = False
            existing_class = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = (existing_class + ' form-control').strip()
            else:
                field.widget.attrs['class'] = (existing_class + ' form-control').strip()

        # Dynamically apply required fields
        print(company)
        if company:
            required_fields = OnboardingDocumentRequirement.objects.filter(
                company=company, is_required=True
            ).values_list('field_name', flat=True)

            # Optional debug print (only in dev)
            print("Required Fields:", list(required_fields))

            for field_name in required_fields:
                if field_name in self.fields:
                    self.fields[field_name].required = True
                else:
                    print(f"⚠ Field '{field_name}' not found in form fields!")
        else:
            print("No company")
            

class OfferResponseForm(forms.ModelForm):
    acknowledgment = forms.BooleanField(required=True, label="I acknowledge the terms and conditions")
    accept = forms.BooleanField(required=False)
    decline = forms.BooleanField(required=False)

    class Meta:
        model = OfferLetters
        fields = ['response']

    def clean(self):
        cleaned_data = super().clean()
        accept = cleaned_data.get('accept')
        decline = cleaned_data.get('decline')

        if not (accept or decline):
            raise forms.ValidationError("You must either accept or decline the offer.")

        if accept and decline:
            raise forms.ValidationError("You cannot both accept and decline the offer.")

        return cleaned_data
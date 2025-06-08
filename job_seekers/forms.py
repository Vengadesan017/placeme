from django import forms
from .models import Candidates, Onboarding, EducationMap, UserLanguages, UserLocations, Employment, Internship, Familys


class CandidatePersonalUpdateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'linkedin_profile', 'country', 'state', 'city',
            'marital_status','languages','work_status'
        ]
        error_messages = {
            'first_name': {
                'required': "First name is required.",
                'max_length': "First name can be at most 255 characters."
            },
            'last_name': {
                'required': "Last name is required.",
                'max_length': "Last name can be at most 255 characters."
            },
            'dob': {
                'required': "Date of birth is required.",
                'invalid': "Enter a valid date in YYYY-MM-DD format."
            },
            'linkedin_profile': {
                'invalid': "Please enter a valid LinkedIn profile URL."
            },
            'pincode': {
                'required': "Pincode is required.",
                'invalid': "Enter a valid pincode."
            }
        }

class CandidateEducationUpdateForm(forms.ModelForm):
    class Meta:
        model = EducationMap
        fields = [
             'edu_id', 'institute', 'year_of_passing', 'score', 'type_id', 'doc'
        ]
        error_messages = {
            'institute': {
                'required': "Institute name is required.",
            },
            'year_of_passing': {
                'required': "Year of passing is required.",
                'invalid': "Enter a valid year."
            },
            'score': {
                'invalid': "Enter a valid score.",
            }
        }

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
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'dob': 'Date of birth',
            'pincode': 'Pincode',
            'linkedin_profile': 'LinkedIn profile',
            # Add others as needed
        }
        error_messages = {
            'first_name': {
                'required': "First name is required.",
                'max_length': "First name can be at most 255 characters."
            },
            'last_name': {
                'required': "Last name is required.",
                'max_length': "Last name can be at most 255 characters."
            },
            'gender': {
                'required': "Gender is required."
            },
            'dob': {
                'required': "Date of birth is required.",
                'invalid': "Enter a valid date in YYYY-MM-DD format."
            },
            'pincode': {
                'required': "Pincode is required.",
                'max_length': "Pincode can be at most 6 digits.",
                'invalid': "Enter a valid pincode."
            },
            'linkedin_profile': {
                'invalid': "Enter a valid LinkedIn profile URL.",
                'max_length': "LinkedIn URL can be at most 255 characters."
            }
        }
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
        
    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['father_name', 'doj']
        
        if self.instance.pk:  # Ensure it's an existing record
            self.instance.save()
        
        if self.instance.pk:  # Ensure it's an existing record
            self.instance.save()
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(None, f"{field.replace('_', ' ').capitalize()} is required.")  # ✅ Adds only the message
        return cleaned_data

    
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
        

        error_messages = {
            'first_name': {
                'required': "First name is required.",
                'max_length': "First name must be at most 255 characters."
            },
            'last_name': {
                'required': "Last name is required.",
                'max_length': "Last name must be at most 255 characters."
            },
            'gender': {
                'required': "Gender is required."
            },
            'dob': {
                'required': "Date of birth is required.",
                'invalid': "Enter a valid date."
            },
            'relationship': {
                'required': "Relationship is required.",
                'max_length': "Relationship must be at most 100 characters."
            },
            'aadhar_no': {
                'required': "Aadhar number is required.",
                'max_length': "Aadhar number must be 12 digits.",
                'invalid': "Enter a valid Aadhar number."
            },
            'mobile_no': {
                'required': "Mobile number is required.",
                'max_length': "Mobile number must be at most 10 digits.",
                'invalid': "Enter a valid mobile number."
            }
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
        error_messages = {
            'language_id': {
                'required': "Language is required."
            },
            'proficiency': {
                'required': "Proficiency level is required.",
                'invalid': "Enter a valid proficiency value."
            }
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
        model = UserLocations
        fields = [
             'location'
        ]
        error_messages = {
            'location': {
                'required': "Location is required.",
                'max_length': "Location name must be at most 255 characters."
            }
        }
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
        error_messages = {
            'present_ctc': {
                'invalid': "Enter a valid present CTC."
            },
            'expected_ctc': {
                'invalid': "Enter a valid expected CTC."
            },
            'notice_period': {
                'max_length': "Notice period must be at most 100 characters."
            }
        }


class CandidateEmploymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = [
             'company_name', 'company_role', 'doj', 'dol', 'type_id','reason_for_leaving', 'doc'
        ]
        error_messages = {
            'company_name': {
                'required': "Company name is required.",
                'max_length': "Company name must be at most 255 characters."
            },
            'company_role': {
                'required': "Role is required.",
                'max_length': "Role must be at most 255 characters."
            },
            'doj': {
                'required': "Date of joining is required.",
                'invalid': "Enter a valid date."
            },
            'dol': {
                'invalid': "Enter a valid date of leaving."
            },
            'reason_for_leaving': {
                'max_length': "Reason must be at most 500 characters."
            }
        }
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
        error_messages = {
            'company_name': {
                'required': "Company name is required.",
                'max_length': "Company name must be at most 255 characters."
            },
            'company_role': {
                'required': "Role is required.",
                'max_length': "Role must be at most 255 characters."
            },
            'doj': {
                'required': "Date of joining is required.",
                'invalid': "Enter a valid date."
            },
            'what_did': {
                'max_length': "Description must be at most 1000 characters."
            }
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
        error_messages = {
            'profile_pic': {
                'required': "Profile picture is required.",
                'invalid_image': "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
                'invalid': "Invalid image format. Please upload a valid image file (e.g., JPG, PNG)."
            }
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
        error_messages = {
            'resume': {
                'required': "Resume file is required.",
                'invalid': "Invalid file format. Please upload a PDF or DOCX file."
            }
        }
    def save(self, commit=True, candidate=None):
        instance = super().save(commit=False)
        if candidate:
            instance.candidate = candidate
        if commit:
            instance.save()
        return instance
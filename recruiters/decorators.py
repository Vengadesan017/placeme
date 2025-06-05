from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

from .models import Companies
from job_seekers.models import Candidates
def is_recruiter(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            if request.user.is_recruiter: 
                return view_func(request, *args, **kwargs)
            messages.info(request, "You must rigister your company or Your company admin must add you as recruiter")
            return redirect('recruiters:create_company')  # Replace with your no-permission page
        messages.info(request, "Please login  or signup")
        return redirect('auth:login')  # Replace with your no-permission page
    return _wrapped_view

def is_kyc(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            candidate = Candidates.objects.get(user=request.user)
            company = Companies.objects.get(candidate=candidate)
            if company.is_kyc_verified:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Your KYC verification is pending.")
                return redirect('recruiters:complete_kyc')  # Replace with your KYC verification page
        except (Candidates.DoesNotExist, Companies.DoesNotExist):
            messages.error(request, "You must be associated with a company.")
            return redirect('error_page')  # Replace with your error page
    return _wrapped_view
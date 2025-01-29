from functools import wraps
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from .forms import CreateCompanyForm, CreateCompanyKYCForm
from .models import Companies
from job_seekers.models import Candidates
from django.contrib import messages

def is_recruiter(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_recruiter:
            return view_func(request, *args, **kwargs)
        messages.info(request, "You must rigister your company or admin add you as recruiter")
        return redirect('recruiters:create_company')  # Replace with your no-permission page
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
                return redirect('no_permission_page')  # Replace with your KYC verification page
        except (Candidates.DoesNotExist, Companies.DoesNotExist):
            messages.error(request, "You must be associated with a company.")
            return redirect('error_page')  # Replace with your error page
    return _wrapped_view


@login_required
def CreateCompany(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        if request.method == "POST":
            if 'create_company' in request.POST:
                form = CreateCompanyForm(request.POST)
                if form.is_valid():
                    form.save(candidate=candidate)
                    messages.info(request,'Your Company was successfully Registered.')
                    try:
                        user = request.user
                        user.is_recruiter = True
                        user.save()
                    except Exception as e:
                        messages.error(request, 'An error occurred while updating your profile.')
                    return redirect('recruiters:complete_kyc') 
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')
        createForm = CreateCompanyForm()
        context = {
            'createForm': createForm,
            'candidate':candidate
        }
        return render(request,'recruiters/create_company.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


# @is_recruiter
def CompleteKYC(request):
    try:
        candidate = Candidates.objects.get(user=request.user)
        company = Companies.objects.get(candidate=candidate)
        if request.method == "POST":
            if 'upload_kyc' in request.POST:
                form = CreateCompanyKYCForm(request.POST, request.FILES,instance=company)
                if form.is_valid():
                    form.save()
                    messages.info(request,'Your KYC was successfully Registered.')
                    return redirect('recruiters:complete_kyc') 
                else:
                    print("Form errors:", form.errors)
                    messages.error(request, 'Please enter the valid data')
        KYCForm = CreateCompanyKYCForm()
        if company.gst_no or company.gst_doc or company.pan_no or company.pan_doc or company.back_ifsc_no or company.bank_account_doc:
            company = False
            print(False)
        else:
            print(True)
        context = {
            'KYCForm': KYCForm,
            'company':company
        }
        return render(request,'recruiters/complete_kyc.html',context)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


@is_recruiter
def Home(request):
    return render(request,'recruiters/layout.html')

@is_recruiter
@is_kyc
def Applications(request):
    return HttpResponse("<h1>view the Candidate's Applications</h1>")

@is_recruiter
@is_kyc
def Jobs(request):
    return HttpResponse("<h1>view or edit Jobs</h1>")

@is_recruiter
@is_kyc
def CreateJob(request):
    return HttpResponse("<h1>CreateJob</h1>")

@is_recruiter
@is_kyc
def Users(request):
    return HttpResponse("<h1>view or edit Users</h1>")

@is_recruiter
@is_kyc
def CreateUser(request):
    return HttpResponse("<h1>CreateUsers</h1>")

@is_recruiter
@is_kyc
def Profile(request):
    return HttpResponse("<h1>view or edit profile</h1>")

@is_recruiter
@is_kyc
def EmployeeLifeCycle(request):
    return HttpResponse("<h1>EmployeeLifeCycle management</h1>")


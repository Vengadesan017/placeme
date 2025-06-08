from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout, authenticate
from django.urls import reverse
from .models import Users
from job_seekers.models import Candidates
from django.contrib.auth import get_user_model
from django.conf import settings
import requests
# from django.contrib.auth.hashers import make_password

from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
# from .forms import CustomAuthenticationForm
from django.http import HttpResponse

from django.utils.http import url_has_allowed_host_and_scheme
import logging

logger = logging.getLogger('auth_logger')

def AuthPage(request):
    return redirect('auth:login')
    

def ratelimited(request, exception):
    logger.warning("Rate limit hit. Redirecting user.", exc_info=exception)
    messages.error(request, "You have exceeded the limit. Please try again later.")
    return redirect('job_seeker:home')


def LogoutPage(request):
    try:
        logout(request)
        return redirect('job_seeker:home')
    except Exception as e:
        logger.exception("logout error:",e)
        messages.error(request, "Something went wrong. Please try again later.")
        return redirect('auth:login')
        

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@csrf_protect
def LoginPage(request):
    try:
        if request.user.is_authenticated:
            next_url = request.GET.get('next') or request.POST.get('next')
            if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = None
            if request.user.is_recruiter:
                return redirect(next_url or "recruiters:home")
            else:
                return redirect(next_url or "job_seeker:home")
            
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            recaptcha_response = request.POST.get('g-recaptcha-response')
            next_url = request.GET.get('next') or request.POST.get('next')
            if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = None
            # referer_url = request.META.get('HTTP_REFERER', '')  # Get the referer URL or default to an empty string
            # print("login----> Referer URL:", referer_url)
            
            
            # --- reCAPTCHA Validation (uncomment if needed) ---
            # payload = {
            #     'secret': settings.RECAPTCHA_PRIVATE_KEY,
            #     'response': recaptcha_response
            # }
            # response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
            # result = response.json()

            # if not result.get('success'):
            #     messages.error(request, 'reCAPTCHA verification failed. Please try again.')
            #     return redirect('auth:login')
                # return render(request,'auth:login.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
            
            
            # Input validation
            if not username or not password:
                messages.error(request, "Enter a valid Username and Password.")
                return redirect('auth:login')

            user=authenticate(request,username=username,password=password)
            if user is not None:
                    auth_login(request,user)
                    
                    if user.is_recruiter:
                        return redirect(next_url or "recruiters:home")
                    else:
                        return redirect(next_url or "job_seeker:home")
                    # if user.is_admin:
                    #     return redirect("administrator:dashboard")  # Admin dashboard
            else:
                messages.error(request, "Invalid Username and Password.")
                return render(request,'auth/login.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
            
                            
        return render(request,'auth/login.html' ,{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
    except Exception as e:
        logger.exception("Login error:",e)
        messages.error(request, "Something went wrong. Please try again later.")
        return redirect("auth:login")



@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@csrf_protect
def SignupPage(request):
    try:
        if request.user.is_authenticated:
            next_url = request.GET.get('next') or request.POST.get('next')
            if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = None
            if request.user.is_recruiter:
                return redirect(next_url or "recruiters:home")
            else:
                return redirect(next_url or "job_seeker:home")
            
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            mobile_no = request.POST.get('mobile_no')
            next_url = request.GET.get('next') or request.POST.get('next')
            
            if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                next_url = None
            # country = request.POST.get('country')
            # state = request.POST.get('state')
            # city = request.POST.get('city')
            recaptcha_response = request.POST.get('g-recaptcha-response')
            # # Recaptcha
            # payload = {
            #     'secret': settings.RECAPTCHA_PRIVATE_KEY,
            #     'response': recaptcha_response
            # }
            # response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
            # result = response.json()

            # if not result.get('success'):
            #     messages.error(request, 'reCAPTCHA verification failed. Please try again.')
            #     return redirect('auth:signup')

            # Validate POST data
            if first_name and last_name and email and password1 and password2 and mobile_no and len(mobile_no) == 10:
                if not Users.objects.filter(email=email).exists():
                    if not Users.objects.filter(mobile_no=mobile_no).exists():
                        try:
                            validate_email(email)
                        except ValidationError:
                            messages.error(request, "Invalid email format.")
                            return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
                        else:
                            if password1==password2:

                                try:
                                    validate_password(password1)
                                except ValidationError as e:
                                    for error in e.messages:
                                        messages.error(request, error)
                                    return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
                                else:
                                    # Create a new user
                                    user = Users.objects.create_user(
                                        email=email,
                                        mobile_no=mobile_no,
                                        password=password1
                                    )

                                    # create candidate
                                    c = Candidates.objects.create(
                                        user=user,
                                        first_name=first_name,
                                        last_name=last_name
                                    )

                                    # # create Onboarding
                                    # Onboarding.objects.create(
                                    #     candidate=c
                                    # )
                                    
                                    user=authenticate(request,username=email,password=password1)
                                    if user is not None:
                                        auth_login(request,user)  # Log the user in after registration
                                        # if user.is_admin:
                                        #     return redirect("administrator:dashboard")  # Admin dashboard
                                        if user.is_recruiter:
                                            return redirect(next_url or "recruiters:home")
                                        else:
                                            return redirect(next_url or "job_seeker:home")                                
                                    else:
                                        messages.error(request, "Your account is created, you need to login here manually.")
                                        return render(request,'auth/login.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})   
                            else:
                                messages.error(request, "Password and Confirm password does not match.")
                                return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})                  

                    else:
                        messages.error(request, "Mobile number has already been used, Try new one.")
                        return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
                else:
                    messages.error(request, "Email has already been used, Try new one.")
                    return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
            else:
                messages.error(request, "Enter all required details.")
                return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})

        if request.user.is_authenticated:
            if request.user.is_recruiter:
                return redirect('recruiters:home')
            else :
                return redirect('job_seeker:home')
        return render(request,'auth/signup.html',{'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY})
    except Exception as e:
        logger.exception("Sign up error:",e)
        messages.error(request, "Something went wrong. Please try again later.")
        return redirect("auth:signup")
    
    
    
    # ======================employer===============




from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

from .models import Onboarding, Candidates



def is_onboarding(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        onboarding_id = kwargs.get("onboarding_id")
        candidate = Candidates.objects.filter(user=request.user).first()
        # print("1 ",candidate)
        if candidate:
            onboarding = Onboarding.objects.filter(candidate=candidate, Onbording_id=onboarding_id).first()
            # print("2 ",onboarding)
            if onboarding:
                if not onboarding.created_date and onboarding.closed:
                    messages.warning(request, "You do not have access to enter the onboarding page.")
                    return redirect('job_seeker:home')
                elif onboarding.is_completed:
                    messages.warning(request, "You have already completed the onboarding process.")
                    return redirect('job_seeker:home')
                else:
                    # print("3 ",onboarding)
                    return view_func(request, *args, **kwargs)
        messages.warning(request, "You do not have access to enter the onboarding page.")
        return redirect('job_seeker:home')
    return _wrapped_view
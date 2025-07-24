from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def status_with_time(application):
    status = application.status
    time = None

    if status == 'Viewed':
        time = application.viewed_at
    elif status == 'Shortlisted':
        time = application.shortlisted_at
    elif status == 'Interviewed':
        time = application.interview_at
    elif status == 'Selected':
        time = application.selected_at
    elif status == 'Offered':
        time = application.offered_at
    elif status == 'Accepted':
        time = application.accepted_at
    elif status == 'Rejected':
        time = application.rejected_at
    elif status == 'Hired':
        time = application.hired_at
    else:
        time = application.applied_date

    if time:
        return f"{status} – {timesince(time)} ago"
    return status



@register.filter
def app_status_time(application):
    status = application.status
    time = None

    if status == 'Viewed':
        time = application.viewed_at
    elif status == 'Shortlisted':
        time = application.shortlisted_at
    elif status == 'Interviewed':
        time = application.interview_at
    elif status == 'Selected':
        time = application.selected_at
    elif status == 'Offered':
        time = application.offered_at
    elif status == 'Accepted':
        time = application.accepted_at
    elif status == 'Rejected':
        time = application.rejected_at
    elif status == 'Hired':
        time = application.hired_at
    else:
        time = application.applied_date

    if time:
        return f"{timesince(time).split(',')[0]} ago"
    return ''

from django.contrib import messages

def form_errors_to_messages(request, form, level='error'):
    for field, errors in form.errors.items():
        label = form.fields.get(field).label if field in form.fields else field
        joined = ' | '.join(errors)
        if level == 'error':
            messages.error(request, f"<strong>{label}</strong>: {joined}")
        elif level == 'warning':
            messages.warning(request, f"<strong>{label}</strong>: {joined}")
        elif level == 'info':
            messages.info(request, f"<strong>{label}</strong>: {joined}")
        elif level == 'success':
            messages.success(request, f"<strong>{label}</strong>: {joined}")
    
            
def form_errors_to_messages_htmx(form, level='error'):
    """
    Returns form errors in a dictionary where each key is a field label,
    and the value is a dict with 'messages' and 'level'.
    """
    errors_dict = {}
    for field, errors in form.errors.items():
        label = form.fields.get(field).label if field in form.fields else field
        joined_errors = ' | '.join(errors)
        errors_dict[label] = {
            "messages": [joined_errors],
            "level": level
        }
    return errors_dict
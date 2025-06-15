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
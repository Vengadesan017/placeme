from django.contrib import messages
from django.forms import BaseFormSet

# def form_errors_to_messages(request, form, level='error'):
#     for field, errors in form.errors.items():
#         label = form.fields.get(field).label if field in form.fields else field
#         joined = ' | '.join(errors)
#         if level == 'error':
#             messages.error(request, f"<strong>{label}</strong>: {joined}")
#         elif level == 'warning':
#             messages.warning(request, f"<strong>{label}</strong>: {joined}")
#         elif level == 'info':
#             messages.info(request, f"<strong>{label}</strong>: {joined}")
#         elif level == 'success':
#             messages.success(request, f"<strong>{label}</strong>: {joined}")
def form_errors_to_messages(request, form_or_formset, level='error'):
    if isinstance(form_or_formset, BaseFormSet):
        for i, form in enumerate(form_or_formset.forms):
            for field, errors in form.errors.items():
                raw_label = form.fields.get(field).label if field in form.fields else field
                label = str(raw_label or field)
                joined = ' | '.join(errors)
                prefix = f"Form {i + 1} - " if len(form_or_formset.forms) > 1 else ""
                _send_message(request, prefix + label, joined, level)
    else:
        for field, errors in form_or_formset.errors.items():
            raw_label = form_or_formset.fields.get(field).label if field in form_or_formset.fields else field
            label = str(raw_label or field)
            joined = ' | '.join(errors)
            _send_message(request, label, joined, level)


def _send_message(request, label, message, level):
    msg = f"<strong>{label}</strong>: {message}"
    if level == 'error':
        messages.error(request, msg)
    elif level == 'warning':
        messages.warning(request, msg)
    elif level == 'info':
        messages.info(request, msg)
    elif level == 'success':
        messages.success(request, msg)
            
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
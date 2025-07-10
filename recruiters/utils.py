from django.contrib import messages
from .models import PositionGroup, Positions

from django.db import transaction

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
            
            
            
def create_bulk_positions(company, title, count, jd, created_by, remarks=None):
    with transaction.atomic():
        last_code = PositionGroup.objects.filter(company=company).order_by('-position_code').values_list('position_code', flat=True).first()
        new_code = last_code + 1 if last_code else 1001

        # Create one PositionGroup
        group = PositionGroup.objects.create(
            company=company,
            position_code=new_code,
            position_title=title,
            jd=jd,
            remarks=remarks,
            created_by=created_by
        )

        # Create N Position rows referencing that group
        for _ in range(count):
            Positions.objects.create(
                position_group=group,
                created_by=created_by
            )

        return group  # or group.positions.all() if needed

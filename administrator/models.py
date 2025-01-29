from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from credentials.models import Users

User = get_user_model()


class AdminUser(models.Model):
    admin_user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='admin_user',blank=True, null=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='admin_user_created_by',blank=True, null=True)
    is_approve = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} ({self.created_at})"

class AdminLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    admin_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='admin_logs',blank=True, null=True)
    action = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.admin_user.email} - {self.action} at {self.timestamp}"


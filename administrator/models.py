from django.db import models
# from django.contrib.auth import get_user_model
from django.utils import timezone
# from credentials.models import Users
# from job_seekers.models import Candidates
from recruiters.models import Companies
from datetime import timedelta

# User = get_user_model()

# =====================================Admin Control Begin========================================================


class AdminUser(models.Model):
    admin_user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('job_seekers.Candidates', on_delete=models.CASCADE, related_name='admin_user',blank=True, null=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='admin_user_created_by',blank=True, null=True)
    is_approve = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} ({self.created_at})"

class AdminLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    admin_user = models.ForeignKey('job_seekers.Candidates', on_delete=models.CASCADE, related_name='admin_logs',blank=True, null=True)
    action = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.admin_user.email} - {self.action} at {self.timestamp}"
# =====================================Admin Control End========================================================

# =====================================Package Begin========================================================

class Packages(models.Model):
    package_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(blank=True,null=True)  # e.g., 30 for monthly

    # Limits for the plan
    max_job_posts = models.PositiveIntegerField(default=10)
    max_resume_downloads = models.PositiveIntegerField(default=50)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='create_package', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    upadted_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='update_package', null=True, blank=True)    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PackageUsage(models.Model):
    package_payment_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companies, on_delete=models.PROTECT)
    package = models.ForeignKey(Packages, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255, unique=True)  # From Stripe/PayPal
    paid_by = models.ForeignKey('job_seekers.Candidates', on_delete=models.PROTECT, related_name='buy_package', null=True, blank=True)
    job_posts= models.PositiveIntegerField(default=0)
    resume_downloads = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True,null=True)
    status = models.TextField(blank=True,null=True)
    # status  = models.CharField(max_length=100, choices=[  # need to change
    #     ('Open', 'Open'),
    #     ('Close', 'Close')

    # ], blank=True, null=True)

    def __str__(self):
        return f"{self.company} - {self.package} - {self.payment_date}"
    
    # def remaining_job_posts(self):
    #     return max(0, self.package.max_job_posts - self.job_posts_used)

    # def remaining_resume_downloads(self):
    #     return max(0, self.package.max_resume_downloads - self.resume_downloads_used)

    # def remaining_messages(self):
    #     return max(0, self.package.plan.max_messages - self.messages_used)
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.job_posts = self.package.max_job_posts
            self.resume_downloads = self.package.max_resume_downloads
            # Save the new instance
            super(PackageUsage, self).save(*args, **kwargs)

        else:
            # Save the Existing instance
            super(PackageUsage, self).save(*args, **kwargs)
    
# =====================================Package End========================================================

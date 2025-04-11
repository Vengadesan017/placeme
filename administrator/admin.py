from django.contrib import admin
from .models import *

admin.site.register(AdminUser)
admin.site.register(AdminLog)

admin.site.register(Packages)
admin.site.register(PackageUsage)
# admin.site.register(Bookmarks)
# admin.site.register(OnbordingDocument)
# admin.site.register(JobApplications)
# admin.site.register(AdditionalInfo)
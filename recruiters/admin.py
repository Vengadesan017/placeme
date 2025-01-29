from django.contrib import admin
from .models import *

admin.site.register(Companies)
admin.site.register(BookmarkCandidates)
admin.site.register(Benefits)
admin.site.register(Commands)
admin.site.register(Jobs)
admin.site.register(SubUserAccess)
admin.site.register(Locations)
admin.site.register(Qualifications)
# admin.site.register(JobsBenefitsMaps)
admin.site.register(CountryForLoc)
admin.site.register(StateForLoc)
admin.site.register(DistrictForLoc)


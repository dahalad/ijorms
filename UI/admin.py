from django.contrib import admin

from . models import Applicant, Job, JobApplicant
# Register your models here.

# Models registered here can be altered by the admins from admin panel
admin.site.register(Applicant)
admin.site.register(Job)
admin.site.register(JobApplicant)
from django.contrib import admin

from .models import Submission,SubmissionHistory

admin.site.register(Submission)
admin.site.register(SubmissionHistory)

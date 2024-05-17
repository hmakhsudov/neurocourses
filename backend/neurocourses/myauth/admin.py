from django.contrib import admin
from .models import CustomUser, PupilProfile, TeacherProfile

admin.site.register(CustomUser)
admin.site.register(PupilProfile)
admin.site.register(TeacherProfile)
from django.contrib import admin
from .models import MedicalAccess, TypeExams, ExamRequest, RequestForExams


admin.site.register(TypeExams)
admin.site.register(ExamRequest)
admin.site.register(RequestForExams)
admin.site.register(MedicalAccess)

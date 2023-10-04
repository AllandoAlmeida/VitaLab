from django.contrib import admin
from .models import TypeExams, ExamRequest, RequestForExams


admin.site.register(TypeExams)
admin.site.register(ExamRequest)
admin.site.register(RequestForExams)

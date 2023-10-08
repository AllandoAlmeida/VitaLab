from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class TypeExams(models.Model):
    type_choices = (("I", "Exame de imagem"), ("S", "Exame de sangue"))
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=type_choices)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()

    def __str__(self):
        return self.name


class ExamRequest(models.Model):
    choice_status = (("E", "Em análise"), ("F", "Finalizado"))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(TypeExams, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    result = models.FileField(upload_to="results", null=True, blank=True)
    requer_password = models.BooleanField(default=False)
    password = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.user} | {self.exam.name}"

    def badge_template(self):
        if self.status == "E":
            css_class = 'bg-warning text-dark'
            text = "Em análise"
        elif self.status == "F":
            css_class = 'bg-success'
            text = "Finalizado"
        return mark_safe(f'<span class="badge {css_class}">{text}</span>')


class RequestForExams(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exams = models.ManyToManyField(ExamRequest)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} | {self.date}'

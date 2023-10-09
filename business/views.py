from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.messages import constants
from exams.models import ExamRequest
from .utils import create_pdf_exam_password, create_random_password


@staff_member_required
def manage_customers(request):
    customers = User.objects.filter(is_staff=False)
    full_name = request.GET.get('name')
    email = request.GET.get('email')

    if email:
        customers = customers.filter(email__contains=email)
    if full_name:
        customers = customers.annotate(
            full_name=Concat(
                'first_name',
                Value(' '),
                'last_name')).filter(full_name__contains=full_name)

        for client in customers:
            print(client.full_name)
            print('-'*10)

    return render(request, 'manage_customers.html', {"customers": customers})


@staff_member_required
def client(request, client_id):
    client = User.objects.get(id=client_id)
    exams = ExamRequest.objects.filter(user=client)
    return render(request, 'client.html', {'client': client, 'exams': exams})


@staff_member_required
def exam_client(request, exam_id):
    exam = ExamRequest.objects.get(pk=exam_id)
    return render(request, 'exam_client.html', {'exam': exam})


def proxy_pdf(request, exam_id):
    exam = ExamRequest.objects.get(pk=exam_id)

    response = exam.result.open()

    return HttpResponse(response)


def generate_exam_password(request, exam_id):
    exam = ExamRequest.objects.get(pk=exam_id)

    if exam.password:
        return FileResponse(create_pdf_exam_password(
            exam.exam.name,
            exam.user.get_full_name,
            exam.password,
        ), filename="token.pdf")

    exam.password = create_random_password(9)
    exam.save()
    return FileResponse(create_pdf_exam_password(
            exam.exam.name,
            exam.user.get_full_name,
            exam.password,
        ), filename="token.pdf")


def change_exam_data(request, exam_id):
    exam = ExamRequest.objects.get(pk=exam_id)

    pdf = request.FILES.get('result')
    status = request.POST.get('status')
    requer_password = request.POST.get('requer_password')

    if requer_password and (not exam.password):
        messages.add_message(
            request,
            constants.ERROR,
            'Atencão: Gere uma senha antes de selecionar'
            ' " Reqquer senha para Acesso ".'
        )
        return redirect(f'/business/exam_client/{exam_id}')

    exam.requer_password = True if requer_password else False

    if pdf:
        exam.result = pdf
    exam.status = status
    exam.save()

    return HttpResponse("alterado")

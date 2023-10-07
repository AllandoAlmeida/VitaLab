from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import RequestForExams, TypeExams, ExamRequest
from django.utils import timezone
from datetime import datetime


@login_required
def request_exams(request):
    date_exams = timezone.now().strftime("%d de %B de %Y")
    type_exams = TypeExams.objects.all()
    if request.method == "GET":
        return render(
            request, "request_exams.html",
            {"type_exames_list": type_exams}
            )
    elif request.method == "POST":
        exams_id = request.POST.getlist("exams")
        request_for_exams = TypeExams.objects.filter(pk__in=exams_id)
        print('request_for_exams', request_for_exams)

        price_total = 0
        for i in request_for_exams:
            if i.available:
                price_total += i.price
        return render(
            request,
            "request_exams.html",
            {
                "type_exames_list": type_exams,
                "request_for_exams": request_for_exams,
                "price_total": price_total,
                "date_exams": date_exams,
            },
        )


def finalize_order(request):
    exams_id = request.POST.getlist("exams")
    request_for_exams = TypeExams.objects.filter(id__in=exams_id)
    
    print("exams_id", exams_id)
    print("request_for_exams", request_for_exams)

    order_exam = RequestForExams(
        user=request.user,
        date=datetime.now()
        )
    
    print("order_exam", order_exam)

    order_exam.save()

    # Crie uma lista para armazenar todos os objetos ExamRequest
    request_exams_list = []

    for exam in request_for_exams:
        request_exams_temp = ExamRequest(
            user=request.user,
            exam=exam,
            status="E"
        )

        # Adicione cada objeto ExamRequest à lista
        request_exams_list.append(request_exams_temp)

    # Salve todos os objetos ExamRequest fora do loop
    for request_exam in request_exams_list:
        request_exam.save()

    return HttpResponse("Finalizar pedido")

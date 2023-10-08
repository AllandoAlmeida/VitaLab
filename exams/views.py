from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RequestForExams, TypeExams, ExamRequest
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


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
        print("request_for_exams", request_for_exams)

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


@login_required
def finalize_order(request):
    exams_id = request.POST.getlist("exams")
    request_for_exams = TypeExams.objects.filter(pk__in=exams_id)

    print("exams_id", exams_id)
    print("request_for_exams", request_for_exams)

    order_exams = RequestForExams(user=request.user, date=datetime.now())

    print("order_exams", order_exams)

    order_exams.save()

    request_exams_list = []

    for exam in request_for_exams:
        request_exams_temp = ExamRequest(
            user=request.user,
            exam=exam, status="E"
        )

    request_exams_list.append(request_exams_temp)
    for request_exam in request_exams_list:
        request_exam.save()
        order_exams.exams.add(request_exam)

    order_exams.save()
    messages.add_message(
        request, constants.SUCCESS, "Pedido de exame Realizado com Sucesso"
    )
    return redirect("/exams/manage_orders/")


@login_required
def manage_orders(request):
    orders_exams = RequestForExams.objects.filter(user=request.user)

    return render(request, "manage_orders.html", {
        "orders_exams":
            orders_exams}
    )


@login_required
def delete_orders(request, order_id):
    order = RequestForExams.objects.get(pk=order_id)
    if not order.user == request.user:
        messages.add_message(
            request,
            constants.ERROR,
            f"Pedido de exame n° {order.id} não pertence ao {request.user}, "
            "portanto você não tem autorização para realizar o cancelamento",
        )
        return redirect("/exams/manage_orders/")

    order.scheduled = False
    order.save()
    messages.add_message(
        request,
        constants.SUCCESS,
        f"Pedido de exame n° {order.id} cancelado com Sucesso",
    )
    return redirect("/exams/manage_orders/")


@login_required
def manage_exams(request):
    exams = ExamRequest.objects.filter(user=request.user)
    return render(request, "manage_exams.html", {"exams": exams})


@login_required
def open_exams_without_password(request, exam_id):
    exam = ExamRequest.objects.get(pk=exam_id)
    if not exam.requer_password:
        return redirect(exam.result.url)
    return redirect(f"/exams/exam_with_password/{exam_id}")


@login_required
def exam_with_password(request, exam_id):
    exam = ExamRequest.objects.get(pk=exam_id)
    if request.method == "GET":
        return render(request, "exam_with_password.html", {"exam": exam})
    elif request.method == "POST":
        password = request.POST.get("password")
        if password == exam.password:
            return redirect(exam.result.url)
        else:
            messages.add_message(
                request,
                constants.ERROR,
                "Senha Inválida",
            )
            return redirect(f"/exams/exam_with_password/{exam_id}")

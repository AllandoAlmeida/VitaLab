from django.urls import path
from . import views

urlpatterns = [
    path('request_exams/', views.request_exams, name="request_exams"),
    path('finalize_order/', views.finalize_order, name="finalize_order"),
    path('manage_orders/', views.manage_orders, name="manage_orders"),
    path(
        'delete_orders/<int:order_id>',
        views.delete_orders,
        name="delete_orders"
    ),
    path('manage_exams/', views.manage_exams, name="manage_exams"),
    path(
        'open_exams_without_password/<int:exam_id>',
        views.open_exams_without_password,
        name="open_exams_without_password"
    ),
    path(
       'exam_with_password/<int:exam_id>',
       views.exam_with_password,
       name="exam_with_password"
    ),
    path(
       'generate_medical_access/',
       views.generate_medical_access,
       name="generate_medical_access"
    ),
    path(
       'doctor_access/<str:token>',
       views.doctor_access,
       name="doctor_access"
    ),
]

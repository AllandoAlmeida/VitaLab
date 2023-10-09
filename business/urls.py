from django.urls import path
from . import views

urlpatterns = [
    path("manage_customers/", views.manage_customers, name="manage_customers"),
    path("client/<int:client_id>", views.client, name="client"),
    path("exam_client/<int:exam_id>", views.exam_client, name="exam_client"),
    path("proxy_pdf/<int:exam_id>", views.proxy_pdf, name="proxy_pdf"),
    path(
        "generate_exam_password/<int:exam_id>",
        views.generate_exam_password,
        name="generate_exam_password"
    ),
    path(
        "change_exam_data/<int:exam_id>",
        views.change_exam_data,
        name="change_exam_data"
    ),
]

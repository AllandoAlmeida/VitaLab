import os
import string
from random import choice, shuffle
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO


def create_random_password(size):
    special_characters = string.punctuation
    characters = string.ascii_letters
    numbers_list = string.digits

    surplus = 0
    qtd = size // 3
    if not size % 3 == 0:
        surplus = size - qtd

    letters = ''
    for i in range(0, qtd + surplus):
        letters += choice(characters)

    numbers = ''
    for i in range(0, qtd):
        numbers += choice(numbers_list)

    special = ''
    for i in range(0, qtd):
        special += choice(special_characters)

    password_open_exam = list(letters + numbers + special)
    shuffle(password_open_exam)

    return ''.join(password_open_exam)


def create_pdf_exam_password(exam, patient, password):
    path_template = os.path.join(
        settings.BASE_DIR,
        'templates/documents/create_random_password.html'
    )
    template_render = render_to_string(
        path_template,
        {
            'exam': exam,
            'patient': patient,
            'password': password
        }
    )

    path_output = BytesIO()
    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output

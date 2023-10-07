from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        password_conformation = request.POST.get("password_conformation")

        if not password == password_conformation:
            messages.add_message(
                request, constants.ERROR,
                "senhas divergentes, digite novamente!"
            )
            return redirect("/users/register/")

        if len(password) < 6:
            messages.add_message(
                request, constants.ERROR,
                "senha deve ter o minimo 6 caracteres!"
            )
            return redirect("/users/register/")

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            messages.add_message(
                request, constants.SUCCESS, "Usuário Cadastrado com sucesso"
            )

        except Exception as e:
            messages.add_message(
                request, constants.ERROR,
                "Erro interno: " + str(e)
            )
            return redirect("/users/register/")

        return redirect("/users/register")


def userlogin(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.add_message(
                request, constants.SUCCESS, "Login realizado com sucesso"
            )
            return redirect("/users/register/")
        else:
            messages.add_message(
                request, constants.ERROR, "Username ou senha inválidos!"
            )
            return redirect("/users/login/")

    return HttpResponse(f"{username} - {password}")

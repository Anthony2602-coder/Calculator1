from django.shortcuts import render


def index(request):
    return render(request, "calc/index.html")


def install(request):
    return render(request, "calc/install.html")

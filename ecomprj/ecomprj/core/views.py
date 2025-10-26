from django.http import HttpResponse
from django.shortcuts import render
from templates import core


def index(request):
    return render(request, "core/index.html")
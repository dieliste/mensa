from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    context = {
    }

    return render(request, 'barometer/index.html', context)

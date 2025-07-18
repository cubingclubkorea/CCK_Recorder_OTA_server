from django.shortcuts import render
from .models import Firmware

# Create your views here.

def index(request):
    return render(request, 'firmware/index.html')

def list(request):
    firmwareList=Firmware.objects.all()
    return render(request, 'firmware/list.html', {'firmwareList': firmwareList})


    
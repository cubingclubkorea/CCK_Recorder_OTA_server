import json
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth import authenticate
from .models import Firmware, Device, RecorderType, Contact
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'firmware/index.html')

def list(request): #요청사항 2 (list.html에서 CCK, KBG를 분리해서 출력하는 기능 구현) - view에서 각 단체별 펌웨어를 분리하여 return하도록 설계
    CCK_Firmware = Firmware.objects.filter(name=RecorderType.CCK_Recorder)
    KBG_Firmware = Firmware.objects.filter(name=RecorderType.KBG_Recorder)
    return render(request, 'firmware/list.html', {
        'CCK_Firmware': CCK_Firmware,
        'KBG_Firmware': KBG_Firmware,
    })

def usage(request):
    return render(request, 'firmware/usage.html')

def contact(request): # 요청사항 3 (contact 데이터베이스 연동)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
    return render(request, 'firmware/contact.html')

@csrf_exempt
def latest_firmware(request, name):
    latest = (
        Firmware.objects
        .filter(name=name)
        .order_by('-version_major', '-version_minor', '-version_patch', '-build_date')
        .first()
    )

    if not latest:
        return JsonResponse({'error': 'No firmware found.'}, status=204)

    data = {
        'version': f"{latest.version_major}.{latest.version_minor}.{latest.version_patch}",
    }

    return JsonResponse(data)

@csrf_exempt
def download_firmware(request, name):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed...'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
        device_id = body.get('device_id')
        device_password = body.get('device_password')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest('Failed to decode JSON body.')

    if not device_id or not device_password:
        return JsonResponse({'error': 'device_id, device_password가 필요합니다.'}, status=400)

    try:
        device = Device.objects.get(device_id=device_id)
    except Device.DoesNotExist:
        return HttpResponseForbidden()

    if not device.check_password(device_password):
        return HttpResponseForbidden()

    try:
        latest = (
            Firmware.objects
            .filter(name=name)
            .order_by('-version_major', '-version_minor', '-version_patch', '-build_date')
            .first()
        )

        if not latest:
            return JsonResponse({'error': 'No firmware found.'}, status=204)
    except Firmware.DoesNotExist:
        return JsonResponse({'error': 'Firmware not exists'}, status=204)

    return FileResponse(
        latest.file.open('rb'),
        as_attachment=True,
        filename=latest.file.name.split('/')[-1]
    )
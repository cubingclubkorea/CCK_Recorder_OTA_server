from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

import os
from django.http import FileResponse
from .jwt_auth import DeviceJWTAuthentication
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
    submitted = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        submitted = True
    return render(request, 'firmware/contact.html', {'submitted': submitted})

class DeviceTokenView(APIView):
    def post(self, request):
        device_id = request.data.get("device_id")
        device_password = request.data.get("device_password")

        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not device.check_password(device_password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # JWT 발급
        token = AccessToken.for_user(device)
        token['device_id'] = device.device_id   # 커스텀 claim 추가
            
        latest = (
            Firmware.objects
            .filter(name=device.device_type)
            .order_by('-version_major', '-version_minor', '-version_patch', '-build_date')
            .first()
        )
        if not latest:
            return Response(
                {
                    "token": str(token),
                    "latest_firmware": None
                }
            )

        return Response(
            {
                "token": str(token),
                "latest_firmware": f"{latest.version_major}.{latest.version_minor}.{latest.version_patch}"
            }
        )

class ProtectedFirmwareDownload(APIView):
    authentication_classes = [DeviceJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        device = request.user  # <- Device 인스턴스
        device_type = device.device_type
        print(device)
        # 해당 타입의 최신 펌웨어 가져오기
        latest = (
            Firmware.objects
            .filter(name=device_type)
            .order_by('-version_major', '-version_minor', '-version_patch', '-build_date')
            .first()
        )
        if not latest:
            return Response({"message": "no firmware exists"}, status=status.HTTP_204_NO_CONTENT)

        firmware_path=latest.file.path
        if not os.path.exists(firmware_path):
            return Response({"message": "no firmware exists"}, status=status.HTTP_204_NO_CONTENT)
    
        return FileResponse(open(firmware_path, 'rb'), as_attachment=True, filename=os.path.basename(firmware_path))

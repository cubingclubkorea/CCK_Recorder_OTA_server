from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Device

class DeviceJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            device_id = validated_token.get("device_id")
            return Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            return None
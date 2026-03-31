from django import forms
from django.contrib import admin
from .models import Firmware, Device, Contact

# Register your models here.
admin.site.register(Firmware)

admin.site.site_header="CCK Recorder Admin Page"
admin.site.index_title="CCK Recorder"
admin.site.site_title="Admin Page"
admin.site.register(Contact) # 요청사항 3 (contact 데이터베이스 연동)

class DeviceAdminForm(forms.ModelForm):
    device_password = forms.CharField(
        label='Device Password',
        widget=forms.PasswordInput(render_value=False),
        required=False
    )

    class Meta:
        model = Device
        fields = '__all__'

    def clean_device_password(self):
        password = self.cleaned_data.get('device_password')
        # 비밀번호 해시화 로직 직접 넣거나, 저장 전 모델 메서드 호출 등
        if password:
            # 평문 비밀번호가 들어오면 해시 처리 후 반환
            from django.contrib.auth.hashers import make_password
            return make_password(password)
        else:
            # 비밀번호를 변경하지 않은 경우 기존값 유지
            return self.instance.device_password

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    form = DeviceAdminForm
    list_display = ('device_id', )
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import os

# 요청사항 1 (CharField -> TextChoices)
class RecorderType(models.TextChoices):
    CCK_Recorder = 'CCK_Recorder', 'CCK Recorder'
    KBG_Recorder = 'KBG_Recorder', 'KBG Recorder'
    # 데이터상 이름과 표시이름 다르게

def firmware_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    version = f"v{instance.version_major}.{instance.version_minor}.{instance.version_patch}"
    new_filename = f"{instance.name}_{version}{ext}"
    return f"firmware/{new_filename}"

class Firmware(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(
        max_length=20,
        choices=RecorderType.choices,
        default=RecorderType.CCK_Recorder,
    )
    version_major=models.IntegerField(default=1)
    version_minor=models.IntegerField(default=1)
    version_patch=models.IntegerField(default=1)
    build_date=models.DateTimeField(auto_now_add=True)
    file=models.FileField(upload_to=firmware_upload_path, blank=True)
    descriptor=models.TextField(blank=True)

    class Meta:
        unique_together=('name', 'version_major', 'version_minor', 'version_patch')
        ordering=['-version_major', '-version_minor', '-version_patch']
    
    def __str__(self):
        return f"{self.name} v{self.version_major}.{self.version_minor}.{self.version_patch}"

class Device(models.Model):
    device_id=models.CharField(max_length=20, primary_key=True)
    device_password=models.CharField(max_length=512)
    device_type=models.CharField(
        max_length=20,
        choices=RecorderType.choices,
        default=RecorderType.CCK_Recorder)

    def set_password(self, raw_password):
        self.device_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.device_password)
    
    def save(self, *args, **kwargs):
        # 이미 해시된 값인지 확인 후, 해시 처리하지 않는 안전장치
        if not self.device_password.startswith('pbkdf2_'):
            self.device_password = make_password(self.device_password)
        super().save(*args, **kwargs)
        
    @property
    def id(self):
        return self.device_id
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True

class Contact(models.Model): # 요청사항 3 (contact 데이터베이스 연동)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return f"{self.name} ({self.email})" #어드민 페이지에서 '이름(이메일) 형식으로 표시되도록 변경

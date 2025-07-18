from django.db import models

# Create your models here.
class Firmware(models.Model):
    name=models.CharField(max_length=100)
    version_major=models.IntegerField(default=1)
    version_minor=models.IntegerField(default=1)
    version_patch=models.IntegerField(default=1)
    build_date=models.DateTimeField(auto_now_add=True)
    file=models.FileField(upload_to='firmwares/')
    descriptor=models.TextField(blank=True)

    class Meta:
        unique_together=('name', 'version_major', 'version_minor', 'version_patch')
        ordering=['-version_major', '-version_minor', '-version_patch']
    
    def __str__(self):
        return f"{self.name} v{self.version_major}.{self.version_minor}.{self.version_patch}"

class Device(models.Model):
    device_id=models.CharField(max_length=20)
    device_password=models.CharField(max_length=50)
    is_online=models.BooleanField()

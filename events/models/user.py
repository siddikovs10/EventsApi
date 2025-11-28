from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)  # ✅ email tasdiqlangan yoki yo‘qligini saqlaydi

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_codes")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)  # kod 10 daqiqa amal qiladi
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

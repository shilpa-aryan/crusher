from django.db import models
from django.contrib.auth.models import AbstractUser

# Extending User Model
USER_TYPE_CHOICES = (
    (1, "Administrator"),
    (2, "Site Manager"),
)
class User(AbstractUser):
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)


#For storing OTPS for a particular user
class PhoneOTP(models.Model):
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    otp = models.CharField(max_length=8,null=True, blank=True)
    count = models.IntegerField(default=0)
    updated_at=models.DateTimeField(auto_now=True)
    validated = models.BooleanField(default=False)

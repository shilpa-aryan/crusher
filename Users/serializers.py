from rest_framework import serializers, status
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from rest_framework.response import Response
from django.http import HttpResponse, Http404

from .models import *


class MyUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = ("pk", "username", "email", "first_name", "last_name", "Role_type")
        read_only_fields = ("email",)


class MyRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    user_type = serializers.IntegerField(required=True, write_only=True)

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "email": self.validated_data.get("email", ""),
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "user_type": self.validated_data.get("user_type", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        try:
            if email:
                PhoneOTP.objects.get(email=email,validated=True)
            if username:
                PhoneOTP.objects.get(phone=username,validated=True)
        except PhoneOTP.DoesNotExist:
            raise Http404("User is not validated")

        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.user_type = self.cleaned_data["user_type"]
        user.save()
        return user


class PhoneSendOTPSerializers(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.IntegerField(required=False)


class PhoneOTPSerializers(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.IntegerField(required=False)
    otp_sent = serializers.CharField()


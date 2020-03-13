from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
from django.core.serializers import serialize
import pyotp
import time
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import pyotp
import time
from datetime import timedelta
import datetime
from django.utils import timezone

from .models import *
from .serializers import *
from .utils import sending_otp

import datetime
from django.utils import timezone

totp = pyotp.TOTP("base32secret3232", interval=240)


class SendingOTP(APIView):
    serializer_class = PhoneSendOTPSerializers

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        phone = request.data.get("phone")
        if email:
            user = User.objects.filter(email=email)
        else:
            user = User.objects.filter(username=phone)
        if user.exists():
            return Response({"status": False, "detail": "user is already registered"})
        else:
            if email:
                old = PhoneOTP.objects.filter(email=email)
            else:
                old = PhoneOTP.objects.filter(phone=phone)

            key = totp.now()
            if not old.exists():
                PhoneOTP.objects.create(email=email, phone=phone, otp=key)
            if old.exists():
                old = old.first()
                count = old.count
                if count == 4:
                    if timezone.now() > old.updated_at + timedelta(minutes=2):
                        msgdata = sending_otp(key, phone, email)
                        if msgdata == True:
                            old.count = 0
                            old.otp = key
                            old.save()
                            return Response(
                                {"status": True, "detail": "OTP sent successfully"}
                            )
                        if msgdata == False:
                            return Response(
                                {"status": False, "detail": "sending otp error"}
                            )
                    else:
                        return Response(
                            {
                                "status": False,
                                "detail": "Sending otp error.Limit exceeded,freezed for 30 minutes",
                            }
                        )
                else:
                    msgdata = sending_otp(key, phone, email)
                    if msgdata == True:
                        old.count = count + 1
                        old.otp = key
                        old.save()
                        return Response(
                            {"status": True, "detail": "OTP sent successfully"}
                        )
                    if msgdata == False:
                        return Response(
                            {"status": False, "detail": "sending otp error",}
                        )


class ValidateOTP(APIView):
    serializer_class = PhoneOTPSerializers

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        phone = request.data.get("phone")
        otp_sent = request.data.get("otp_sent")
        if email and otp_sent:
            old = PhoneOTP.objects.filter(email=email)
            user = User.objects.filter(email=email)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone=phone)
            user = User.objects.filter(username=phone)
        

        if old.exists():
            old = old.first()
            otp = old.otp
            if str(otp_sent) == str(otp):
                if totp.verify(otp_sent):
                    tokenizer = 0
                    for i in user:
                        token = Token.objects.filter(user=i.id)
                        for j in token:
                            tokenizer = j.pk
                    content = {
                                "status": True,
                                "detail": "OTP MATCHED.",
                                "token" : tokenizer,
                            }
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"status": False, "detail": "Time expired for otp resend again"}
                    )

            else:
                return Response({"status": False, "detail": "OTP INCORRECT"})
        else:
            return Response(
                {"status": False, "detail": "First proceed via sending otp request",}
            )


class Forgot_password(APIView):
    serializer_class = PhoneSendOTPSerializers
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        phone = request.data.get("phone")
        if email:
            user = User.objects.filter(email=email)
        else:
            user = User.objects.filter(username=phone)
        if not user.exists():
            return Response({"status": False, "detail": "user is not registered"})
        else:
            if email:
                old = PhoneOTP.objects.filter(email=email)
            if phone:
                old = PhoneOTP.objects.filter(phone=phone)

            key = totp.now()
            if old.exists():
                old = old.first()
                count = old.count
                if count == 4:
                    if timezone.now() > old.updated_at + timedelta(minutes=2):
                        msgdata = sending_otp(key, phone, email)
                        if msgdata == True:
                            old.count = 0
                            old.otp = key
                            old.save()
                            return Response(
                                {"status": True, "detail": "OTP sent successfully"}
                            )
                        if msgdata == False:
                            return Response(
                                {"status": False, "detail": "sending otp error",}
                            )
                    else:
                        return Response(
                            {
                                "status": False,
                                "detail": "Sending otp error.Limit exceeded, freezed for 30 minutes",
                            }
                        )
                else:
                    msgdata = sending_otp(key, phone, email)
                    if msgdata == True:
                        old.count = count + 1
                        old.otp = key
                        old.save()
                        return Response(
                            {"status": True, "detail": "OTP sent successfully"}
                        )
                    if msgdata == False:
                        return Response(
                            {"status": False, "detail": "sending otp error",}
                        )




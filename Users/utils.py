from django.conf import settings
from django.core.mail import send_mail
import requests


api_key = "873c3948-523f-11ea-9fa5-0200cd936042  "


def sending_otp(key, phone, email):
    if email:
        message = "Your One Time Password is " + str(key) + "."
        from_email = settings.EMAIL_HOST_USER
        data = send_mail("OTP Validation", message, from_email, [email])
        return True

    if phone:
        # url = "https://2factor.in/API/V1/" + api_key + "/SMS/" + phone + "/" + key
        # response = requests.get(url)
        # smsdata = response.json()
        # if not smsdata["Status"] == "Success":
        #     return False
        return True

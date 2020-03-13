from django.urls import path, include

from .views import *
# handler404 = 'Users.views.myError'


urlpatterns = [
    path("send_otp/", SendingOTP.as_view()),
    path("validate_otp/", ValidateOTP.as_view()),
    path("forgot_password/send_otp/", Forgot_password.as_view()),
]

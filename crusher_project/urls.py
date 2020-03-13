"""crusher_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from allauth.account.views import ConfirmEmailView

from django.urls import path, include
from django.conf.urls import url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from crusher_app.views import *



urlpatterns = [
    path("admin/", admin.site.urls),
    # url(r'^', include('django.contrib.auth.urls')),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    # Override urls
    # url(r'^registration/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
    # url(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
    #     name='account_confirm_email'),
    # url(r'^registration/complete/$', complete_view, name='account_confirm_complete'),
    # url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     null_view, name='password_reset_confirm'),
    # url(r'', include('rest_auth.urls')),
    # url(r'^registration/', include('rest_auth.registration.urls')),
    path("api/", include("crusher_app.urls")),
    path("api/", include("Users.urls")),
    
    # path('email-check-for-registration', EmailCheckView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()


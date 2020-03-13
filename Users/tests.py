from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import *


class SendingOTPTestCases(TestCase):
        
    #Case 1: if sending otp successfull for phone
    def test_sendingOTP_case1(self):
        data = {
                'phone': '8095201186'
            }
        response = self.client.post('/api/send_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)

    #Case 2: if sending otp limit exceeded for phone
    def test_sendingOTP_case2(self):
        PhoneOTP.objects.create(phone="8095201186",otp=5657,count=4)
        data = {
                'phone': '8095201186'
            }
        response = self.client.post('/api/send_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],False)

    #Case 3: if sending otp successfull for email
    def test_sendingOTP_case3(self):
        data = {
                'email': 'shilpa@mailinator.com'
            }
        response = self.client.post('/api/send_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
    
    #Case 4: if sending otp limit exceeded for email
    def test_sending_case4(self):
        PhoneOTP.objects.create(email="shilpa@mailinator.com",otp=5657,count=4)
        data = {
                'email': 'shilpa@mailinator.com'
            }
        response = self.client.post('/api/send_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],False)

class ValidatingOTPTestCases(TestCase):

    #Case 1:Validating OTP if successfull for email
    def test_validate_otp_case1(self):
        data = { 'email': 'shilpa@mailinator.com' }
        response = self.client.post('/api/send_otp/', data, format='json')

        otp=PhoneOTP.objects.get(email=data['email'])

        data = {
                'email': 'shilpa@mailinator.com',
                'otp_sent':otp.otp,
            }
        response = self.client.post('/api/validate_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],True)
 
    #Case 2:Validating OTP if entered incorrect OTP for email
    def test_validate_otp_case2(self):
        PhoneOTP.objects.create(email='shilpa@mailinator.com',otp='874673')
        data = {
                'email': 'shilpa@mailinator.com',
                'otp_sent':'967839',
            }
        response = self.client.post('/api/validate_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],False)

    #Case 3:Validating OTP if successfull for phone
    def test_validate_otp_case3(self):
        data = { 'phone': '8095201186' }
        response = self.client.post('/api/send_otp/', data, format='json')
        otp=PhoneOTP.objects.get(phone=data['phone'])

        data = {
                'phone': '8095201186',
                'otp_sent':otp.otp,
            }
        response = self.client.post('/api/validate_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],True)
 
    #Case 3:Validating OTP if entered incorrect OTP for phone
    def test_validate_otp_case4(self):
        PhoneOTP.objects.create(phone='8095201186',otp='874673')
        data = {
                'phone': '8095201186',
                'otp_sent':'967839',
            }
        response = self.client.post('/api/validate_otp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'],False)

class RegistrationTestsUsingPhoneNumber(TestCase):

    #Setting up the credentials for creating OTP
    def setUp(self):
        self.credentials = {
            'phone':'8095201186',
            'otp': 123456,
            'validated':True}
        PhoneOTP.objects.create(**self.credentials)

    #Case 1:If user registered successfully
    def test_registration_case1(self):
        data = {
                'username': '8095201186',
                "password1":"shilpa123@",
                "password2":"shilpa123@",
                "first_name":"shilpa",
                "last_name":"varu",
                "user_type":1 
                }
        response = self.client.post('/rest-auth/registration/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username,data['username'])
        self.assertEqual(User.objects.get().first_name,data['first_name'])
        self.assertEqual(User.objects.get().last_name,data['last_name'])
        self.assertEqual(User.objects.get().user_type,data['user_type'])

    #Case 2:If user registered with invalid details
    def test_registration_case2(self):
        data = {
                'username': '8095201186',
                "password1":"shilpa123@",
                "password2":"shilpa123@", 
                "first_name":"shilpa",
                "last_name":"varu",
                # "user_type":1 
                }
        response = self.client.post('/rest-auth/registration/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RegistrationTestsUsingEmail(TestCase):

    #Setting up the credentials for creating OTP
    def setUp(self):
        self.credentials = {
            'email':'shilpa@gmail.com',
            'otp': 123456,
            'validated':True,
        }
        PhoneOTP.objects.create(**self.credentials)

    #Case 1:If user registered successfully
    def test_registration_case1(self):
        data = {
                'email': 'shilpa@gmail.com',
                "password1":"shilpa123@",
                "password2":"shilpa123@",
                "first_name":"shilpa",
                "last_name":"varu",
                "user_type":1 
                }
        response = self.client.post('/rest-auth/registration/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().email,data['email'])
        self.assertEqual(User.objects.get().first_name,data['first_name'])
        self.assertEqual(User.objects.get().last_name,data['last_name'])
        self.assertEqual(User.objects.get().user_type,data['user_type'])
    
    #Case 2:If user registered with invalid details
    def test_registration_case2(self):
        data = {
                'email': 'shilpa@gmail.com',
                "password1":"shilpa123@",
                "password2":"shilpa123@", 
                "first_name":"shilpa",
                "last_name":"varu",
                # "user_type":1 
                }
        response = self.client.post('/rest-auth/registration/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#Registration without validation
class RegistrationTests(TestCase):

    #case 1:Registration using phone_number without validation
    def test_registration_case1(self):
        data = {
                'username': '8095201186',
                "password1":"shilpa123@",
                "password2":"shilpa123@",
                "first_name":"shilpa",
                "last_name":"varu",
                "user_type":1 
                }
        response = self.client.post('/rest-auth/registration/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #case 2:Registration using email adress without validation
    def test_registration_case2(self):
            data = {
                    'email': 'shilpa@gmail.com',
                    "password1":"shilpa123@",
                    "password2":"shilpa123@",
                    "first_name":"shilpa",
                    "last_name":"varu",
                    "user_type":1 
                    }
            response = self.client.post('/rest-auth/registration/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#Login TestCases
class LogInTest(TestCase):

    #Setting up the credentials and registering user 
    def setUp(self):
        self.credentials = {
            'username':'8095201186',
            'password': 'shilpa123'}
        User.objects.create_user(**self.credentials)

    #If Login successfull
    def test_login(self):
        response = self.client.post('/rest-auth/login/', self.credentials, follow=True)
        if response.data['key']:
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    

from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import *
import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()



class VehicleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testing", last_name="kar",password='test@123',email="test@gmail.com",user_type=1)
        self.user.set_password('test@123')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        
    def test_create_vehicle(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=89778778
        )
        data = {"vehicle_number": "KA26754", "driver_id": driver.id}
        response = self.client.post("/api/vehicle/registration/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.get().vehicle_number, "KA26754")
        self.assertEqual(Vehicle.objects.get().driver_id, driver)
 
    def test_get_vehicle(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=89778778
        )
        vehicle = Vehicle.objects.create(vehicle_number="ka4546", driver_id=driver)

        url = "/api/vehicle/retrieve/" + str(vehicle.id) + "/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_vehicle_details(self):
        driver_one = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=89778778
        )
        driver_two = Driver.objects.create(
            first_name="test", last_name="code", phone_number=9999999999
        )
        vehicle1 = Vehicle.objects.create(vehicle_number="KA1234", driver_id=driver_one)
        vehicle2 = Vehicle.objects.create(vehicle_number="KA4456", driver_id=driver_two)

        response = self.client.get("/api/vehicle/list/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editing_vehicle_detail(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811118778
        )
        vehicle = Vehicle.objects.create(vehicle_number="ka4546", driver_id=driver)
        url = "/api/vehicle/edit/" + str(vehicle.id) + "/"
        data = {"vehicle_number": "KA99855"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vehicle.objects.get().vehicle_number, "KA99855")

    def test_delete_vehicle_detail(self):
        driver = Driver.objects.create(
            first_name="aaao", last_name="bbb", phone_number=89778778
        )
        vehicle = Vehicle.objects.create(vehicle_number="ka4546", driver_id=driver)
        url = "/api/vehicle/delete/" + str(vehicle.id) + "/"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vehicle_driverId_unique(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811118778
        )
        vehicle = Vehicle.objects.create(vehicle_number="ka4546", driver_id=driver)
        data = {"vehicle_number": "ka4546", "driver_id": driver.id}
        response = self.client.post("/api/vehicle/registration/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DriverTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testing", last_name="kar",password='test@123',email="test@gmail.com",user_type=1)
        self.user.set_password('test@123')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
    
    def test_create_driver(self):
        data = {
            "first_name": "kommindala",
            "last_name": "kartik",
            "phone_number": 8919140556,
        }
        response = self.client.post("/api/driver/add/", data, format="json")
        res= response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res['first_name'], "kommindala")
        self.assertEqual(res['last_name'], "kartik")
        self.assertEqual(res['phone_number'], 8919140556)

    def test_get_driver(self):
        driver = Driver.objects.create(
            first_name="kommindala", last_name="kartik", phone_number=8919140556
        )
        url = "/api/driver/retrieve/" + str(driver.id) + "/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_driver_details(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=89778778
        )
        driver1 = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=892778778
        )
        response = self.client.get("/api/vehicle/list/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editing_driver(self):
        driver = Driver.objects.create(
            first_name="kommindala", last_name="kartik", phone_number=89140556
        )
        url = "/api/driver/edit/" + str(driver.id) + "/"
        data = {
            "first_name": "kommindal",
            "last_name": "kar",
        }
        response = self.client.patch(url, data, format="json")
        res = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Driver.objects.get().first_name, "kommindal")
        self.assertEqual(Driver.objects.get().last_name, "kar")

    def test_delete_driver_detail(self):
        driver = Driver.objects.create(
            first_name="shine", last_name="nn", phone_number=8096201186
        )
        url = "/api/driver/delete/" + str(driver.id) + "/"
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_driver_phone_number_is_unique(self):
        driver1 = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811118778
        )

        data = {
            "first_name": "kommindala",
            "last_name": "kartik",
            "phone_number": 811118778,
        }
        response = self.client.post("/api/driver/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TripTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testing", last_name="kar",password='test@123',email="test@gmail.com",user_type=2)
        self.user.set_password('test@123')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
    def test_create_Trip(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811018664
        )
        data = {"vehicle_number": "kA1542", "tare_weight": 345, "driver_id": driver.id}
        url = "/api/trip/add/"
        response = self.client.post(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.get().vehicle_number, "kA1542")
        self.assertEqual(Trip.objects.get().tare_weight, 345)
        self.assertEqual(Trip.objects.get().gross_weight, None)
        self.assertEqual(Trip.objects.get().driver_id, driver)

    def test_retrieve_Trip(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811018664
        )
        trip = Trip.objects.create(
            vehicle_number="Ka6568", tare_weight=123, driver_id=driver
        )
        url = "/api/trip/retrieve/" + str(trip.id) + "/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Trip.objects.get().vehicle_number, "Ka6568")
        self.assertEqual(Trip.objects.get().tare_weight, 123)
        self.assertEqual(Trip.objects.get().driver_id, driver)

    def test_list_Trip(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811018664
        )
        trip1 = Trip.objects.create(
            vehicle_number="Ka6568", tare_weight=123, driver_id=driver
        )
        trip2 = Trip.objects.create(
            vehicle_number="KA9868", tare_weight=209, driver_id=driver
        )
        url = "/api/trip/list/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_Trip(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811018664
        )
        trip = Trip.objects.create(
            vehicle_number="Ka6568", tare_weight=123, driver_id=driver
        )
        url = "/api/trip/delete/" + str(trip.id) + "/"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_Trip(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811018664
        )
        trip = Trip.objects.create(
            vehicle_number="Ka6568", tare_weight=123, driver_id=driver
        )
        data = {"tare_weight": 200}
        url = "/api/trip/edit/" + str(trip.id) + "/"
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Trip.objects.get().tare_weight, 200)

    def test_draft_Trip(self):
        driver = Driver.objects.create(
            first_name="aaa", last_name="bbb", phone_number=811018664
        )
        trip1 = Trip.objects.create(
            vehicle_number="Ka6568", tare_weight=123, driver_id=driver
        )
        trip2 = Trip.objects.create(
            vehicle_number="Ka6568", tare_weight=130, driver_id=driver
        )
        data = {"vehicle_number": "Ka6568"}

        url = "/api/trip/drafts/"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data.get('trip_details')[0].get('fields').get('tare_weight'), 130)

        def test_draft_Trip_when_data_isNot_present(self):
            data = {"vehicle_number": "Ka6568"}
            url = "/api/trip/drafts/"
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HoursTrackingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testing", last_name="kar",password='test@123',email="test@gmail.com",user_type=2)
        self.user.set_password('test@123')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
    def test_create_Hours(self):
        data = {
            "primary_start_reading": 123,
            "primary_end_reading": 200,
            "secondary_start_reading": 200,
            "secondary_end_reading": 300,
        }
        response = self.client.post("/api/hours/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HoursTracking.objects.get().primary_start_reading, 123)
        self.assertEqual(HoursTracking.objects.get().primary_end_reading, 200)
        self.assertEqual(HoursTracking.objects.get().secondary_start_reading, 200)
        self.assertEqual(HoursTracking.objects.get().secondary_end_reading, 300)

    def test_get_HourTrackingDetail(self):
        HoursTrack = HoursTracking.objects.create(
            primary_start_reading=120.8,
            primary_end_reading=250,
            secondary_start_reading=190.3,
            secondary_end_reading=270.5,
        )
        url = "/api/hours/retrieve/" + str(HoursTrack.id) + "/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editing_HourTrackingDetail(self):
        HoursTrack = HoursTracking.objects.create(
            primary_start_reading=120.8,
            primary_end_reading=300,
            secondary_start_reading=190.3,
            secondary_end_reading=250,
        )
        url = "/api/hours/edit/" + str(HoursTrack.id) + "/"
        data = {"primary_end_reading": 380, "secondary_end_reading": 200.7}
        response = self.client.patch(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HoursTracking.objects.get().primary_end_reading, 380)
        self.assertEqual(HoursTracking.objects.get().secondary_end_reading, 200.7)

    def test_delete_HourTrackingDetail(self):
        HoursTrack = HoursTracking.objects.create(
            primary_start_reading=120.8,
            primary_end_reading=300,
            secondary_start_reading=190.3,
            secondary_end_reading=250,
        )
        url = "/api/hours/delete/" + str(HoursTrack.id) + "/"
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_HourTrackingPreviousReading(self):
        HoursTrack = HoursTracking.objects.create(
            primary_start_reading=120.8,
            primary_end_reading=250,
            secondary_start_reading=190.3,
            secondary_end_reading=270.5,
        )
        url = "/api/hours/retrieve/previous_reading/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_HourTrackingPreviousReading1(self):
        url = "/api/hours/retrieve/previous_reading/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProductionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testing", last_name="kar",password='test@123',email="test@gmail.com",user_type=2)
        self.user.set_password('test@123')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        
    def test_create_production_data(self):
        data = {
            "dust": 10,
            "six_mm": 20,
            "twelve_mm": 30,
            "twenty_mm": 40,
            "forty_mm": 50,
            "sixty_mm": 60,
            "wetmix": 70,
            "gravel": 80,
            "gsb": 90,
            "remarks": "Test production",
        }
        response = self.client.post("/api/production/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DayProduction.objects.get().dust, 10)
        self.assertEqual(DayProduction.objects.get().six_mm, 20)
        self.assertEqual(DayProduction.objects.get().twelve_mm, 30)
        self.assertEqual(DayProduction.objects.get().twenty_mm, 40)
        self.assertEqual(DayProduction.objects.get().forty_mm, 50)
        self.assertEqual(DayProduction.objects.get().sixty_mm, 60)
        self.assertEqual(DayProduction.objects.get().wetmix, 70)
        self.assertEqual(DayProduction.objects.get().gravel, 80)
        self.assertEqual(DayProduction.objects.get().gsb, 90)
        self.assertEqual(DayProduction.objects.get().remarks, "Test production")

    def test_edit_production_data(self):
        DayProd = DayProduction.objects.create(
            dust=10,
            six_mm=20,
            twelve_mm=30,
            twenty_mm=40,
            forty_mm=50,
            sixty_mm=60,
            wetmix=70,
            gravel=80,
            gsb=90,
            remarks="Test production",
        )
        url = "/api/production/edit/" + str(DayProd.id) + "/"
        data = {
            "dust": 30,
            "six_mm": 40,
            "twelve_mm": 30,
            "twenty_mm": 40,
            "forty_mm": 50,
            "sixty_mm": 60,
            "wetmix": 70,
            "gravel": 80,
            "gsb": 90,
            "remarks": "Test production",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DayProduction.objects.get().dust, 30)
        self.assertEqual(DayProduction.objects.get().six_mm, 40)
        self.assertEqual(DayProduction.objects.get().twelve_mm, 30)
        self.assertEqual(DayProduction.objects.get().twenty_mm, 40)
        self.assertEqual(DayProduction.objects.get().forty_mm, 50)
        self.assertEqual(DayProduction.objects.get().sixty_mm, 60)
        self.assertEqual(DayProduction.objects.get().wetmix, 70)
        self.assertEqual(DayProduction.objects.get().gravel, 80)
        self.assertEqual(DayProduction.objects.get().gsb, 90)
        self.assertEqual(DayProduction.objects.get().remarks, "Test production")

    def test_delete_production_data(self):
        DayProd = DayProduction.objects.create(
            dust=10,
            six_mm=20,
            twelve_mm=30,
            twenty_mm=40,
            forty_mm=50,
            sixty_mm=60,
            wetmix=70,
            gravel=80,
            gsb=90,
            remarks="Test production",
        )
        url = "/api/production/delete/" + str(DayProd.id) + "/"
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


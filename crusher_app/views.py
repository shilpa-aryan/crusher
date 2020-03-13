# Django
from rest_framework.views import APIView
from django.core.serializers import serialize
from rest_framework import generics, status
from rest_framework import filters
from crusher_app.serializers import *
from django.views.defaults import bad_request
from django.contrib.auth import get_user_model
from rest_framework.response import Response
import json
from django.core import serializers
from django.http import Http404
from datetime import date
from django.db import IntegrityError
from rest_framework.decorators import api_view
from django.db.models import Q

# local Django
from .models import *
from .permissions import *
User = get_user_model()

class VehicleAssigned(APIView):

    def get(self,request):
        vehicle = Vehicle.objects.all().values('vehicle_number','driver_id__first_name','driver_id__last_name','driver_id__phone_number')
        return Response(vehicle, content_type='application/json')


User=get_user_model()

class VehicleCreateListAPIView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    permission_classes = [IsAdmin]
    


class VehicleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    permission_classes = [IsAdmin]

    def delete(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        if Vehicle.objects.filter(pk=pk).exists():
            Vehicle.objects.filter(pk=pk).delete()
            content = {"success": "True"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"error": "The resource was not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND,)


class VehicleSearchAPIView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    permission_classes = [IsAdmin]

    filter_backends = [filters.SearchFilter]
    search_fields = ["vehicle_number"]


class AddDriver(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    # permission_classes = [IsAdmin]


class RetrieveUpdateDeleteDriver(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdmin]

    def delete(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        if Driver.objects.filter(pk=pk).exists():
            Driver.objects.filter(pk=pk).delete()
            content = {"success": "True"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"error": "The resource was not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND,)


class SearchDriver(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "phone_number"]
    permission_classes = [IsAdmin]


class HoursTrackingCreateListAPIView(generics.ListCreateAPIView):
    queryset = HoursTracking.objects.all()
    serializer_class = HoursTrackingSerializers
    permission_classes = [IsSiteManager]

    def create(self, request, *args, **kwargs):
        try:
            return super(generics.ListCreateAPIView, self).create(
                request, *args, **kwargs
            )
        except IntegrityError:
            content = {"error": "The batch_id already exists"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    
class HoursTrackingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HoursTracking.objects.all()
    serializer_class = HoursTrackingSerializers
    permission_classes = [IsSiteManager]

    def delete(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        if HoursTracking.objects.filter(pk=pk).exists():
            HoursTracking.objects.filter(pk=pk).delete()
            content = {"success": "True"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"error": "The resource was not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class HoursTrackingListOfPrevDataAPIView(generics.ListAPIView):
    queryset = HoursTracking.objects.all()
    serializer_class = HoursTrackingSerializers
    permission_classes = [IsSiteManager]

    def get(self, request, *args, **kwargs):

        if HoursTracking.objects.exists():
            primaryreading = HoursTracking.objects.filter(
                ~Q(primary_end_reading=0)
            ).last()
            secondaryreading = HoursTracking.objects.filter(
                ~Q(secondary_end_reading=0)
            ).last()
            primaryreading = primaryreading.primary_end_reading
            secondaryreading = secondaryreading.secondary_end_reading
            content = {
                "success": "True",
                "primary_end_reading": primaryreading,
                "secondary_end_reading": secondaryreading,
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"success": "False"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class AddTrip(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    # permission_classes = [IsSiteManager]


class RetrieveUpdateDeleteTrip(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsSiteManager]

    def delete(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        if Trip.objects.filter(pk=pk).exists():
            Trip.objects.filter(pk=pk).delete()
            content = {"success": "True"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"error": "The resource was not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND,)


class TripDraft(APIView):
    def post(self, request):
        pk = request.data["vehicle_number"]
        if Trip.objects.filter(vehicle_number=pk):
            trip_data = Trip.objects.filter(vehicle_number=pk).last()
            trip_data = trip_data.id
            trip_data = Trip.objects.filter(id=trip_data)
            trip_data = serialize("json", trip_data)
            trip_data = json.loads(str(trip_data))
            content = {"success": "True", "trip_details": trip_data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"success": "False", "error": "The resource was not found"}
            return Response(
                content,
                status=status.HTTP_404_NOT_FOUND,
                content_type="application/json",
            )


class ProductionCreateList(generics.ListCreateAPIView):
    queryset = DayProduction.objects.all()
    serializer_class = ProductionSerializer
    permission_classes = [IsSiteManager]
    
    def create(self, request, *args, **kwargs):
        try:
            return super(generics.ListCreateAPIView, self).create(
                request, *args, **kwargs
            )
        except IntegrityError:
            content = {"error": "The batch_id already exists"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ProductionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayProduction.objects.all()
    serializer_class = ProductionSerializer
    permission_classes = [IsSiteManager]



    def delete(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        if DayProduction.objects.filter(pk=pk).exists():
            DayProduction.objects.filter(pk=pk).delete()
            content = {"success": "True"}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"error": "The resource was not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND,)


class DayIn(APIView):
    def post(self, request):
        batch_id = request.data["batch_id"]
        data = Trip.objects.filter(batch_id=batch_id)
        dayin = 0
        for i in data:
            if i.gross_weight != None and int(i.gross_weight) != 0:
                dayin += i.gross_weight - i.tare_weight
        if dayin != 0:
            content = {"success": "True", "DayIn": dayin}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"success": "False", "DayIn": "No details found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        
class CheckUserType(generics.ListAPIView):
    
    def get(self,request): 
        k = self.request.user.id
        use = User.objects.filter(id=k)
        try:
            if use[0].user_type == 1:
                content = {"success": "True","User_Type":"Adminstrator"}
                return Response(content, status=status.HTTP_200_OK)
            if use[0].user_type == 2:
                content = {"success": "True","User_Type":"Site Manager"}
                return Response(content, status=status.HTTP_200_OK)
        except:
            content = {"success": "False","message":"Token is not provided"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
                

       

class DayIn(APIView):
    def post(self, request):
        batch_id = request.data["batch_id"]
        data=Trip.objects.filter(batch_id=batch_id)
        dayin=0
        for i in data:
            if (i.gross_weight != None and int(i.gross_weight)!=0):
                dayin+=(i.gross_weight-i.tare_weight)
        if dayin != 0:
            content = {"success": "True","DayIn":dayin}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"success": "False","DayIn":"No details found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class EmailCheckView(APIView):
    def post(self, request):
        x = request.data['email']
        if User.objects.filter(email=x).exists():
            content = {"success": "True", "detail": "email exist" }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {"success": "False", "detail": "email not exist" }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")


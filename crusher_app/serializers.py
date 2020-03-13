from rest_framework import serializers
import datetime
from .models import *


class VehicleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class HoursTrackingSerializers(serializers.ModelSerializer):
    class Meta:
        model = HoursTracking
        fields = ('id','batch_id','primary_start_reading','primary_end_reading','primary_comment','primary_reading','secondary_start_reading','secondary_end_reading','secondary_comment','secondary_reading')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id','batch_id','vehicle_number','trip_number','tare_weight','tare_weight_time','gross_weight','gross_weight_time','net_weight')


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayProduction
        fields = ('id','batch_id','dust','six_mm','twelve_mm','twenty_mm','forty_mm','sixty_mm','wetmix','gravel','gsb','remarks','day_out')

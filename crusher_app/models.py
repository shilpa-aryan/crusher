from django.db import models
from .validators import validate_file_size
from django.contrib import admin
import datetime



from PIL import Image
from django.utils import timezone

# Adding Driver details
class Driver(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone_number = models.CharField(unique=True,max_length=15)
    profile_pic = models.ImageField(blank=True)
    driver_id_doc = models.FileField(blank=True, validators=[validate_file_size])
    driver_licence_doc = models.FileField(blank=True, validators=[validate_file_size])

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

# Adding Vehicle details
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_registration_doc = models.FileField(
        blank=True, null=True, validators=[validate_file_size]
    )
    vehicle_insurance_doc = models.FileField(
        blank=True, null=True, validators=[validate_file_size]
    )
    driver_id = models.OneToOneField(
        Driver, null=True, blank=True,on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.vehicle_number

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

# Adding Dayin
class Trip(models.Model):
    vehicle_number = models.CharField(max_length=20)
    trip_number = models.IntegerField(blank=True)
    batch_id = models.DateField(auto_now_add=True)
    tare_weight = models.IntegerField()
    tare_weight_time = models.DateTimeField(auto_now_add=True)
    gross_weight = models.IntegerField(blank=True, null=True)
    gross_weight_time = models.DateTimeField(auto_now=True) 
    trip_completed = models.BooleanField(default=False)
    driver_id = models.ForeignKey(Driver, null=True, blank=True,on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.trip_number = (
            Trip.objects.filter( 
                batch_id__month=datetime.datetime.today().month,
                batch_id__year=datetime.datetime.today().year,
            ).count()
            + 1
        )

        if (self.tare_weight and self.gross_weight) != None:
            self.trip_completed = True
        super(Trip, self).save(*args, **kwargs)
    @property
    def net_weight(self):
        if self.tare_weight and self.gross_weight :
            net_weight=self.gross_weight-self.tare_weight
            return net_weight
        else:
            return None

    def __str__(self):
        return self.vehicle_number

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"


class HoursTracking(models.Model):
    batch_id = models.DateField(auto_now_add=True, unique=True)
    primary_start_reading = models.FloatField(blank=True)
    primary_end_reading = models.FloatField(null=True, blank=True)
    primary_comment = models.TextField(null=True, blank=True)
    secondary_start_reading = models.FloatField(blank=True)
    secondary_end_reading = models.FloatField(null=True, blank=True)
    secondary_comment = models.TextField(null=True, blank=True)

    @property
    def primary_reading(self):
        if self.primary_end_reading and self.primary_start_reading:
            primary_reading=(self.primary_end_reading-self.primary_start_reading)/24
            return primary_reading
        else:
            return None
   
    @property
    def secondary_reading(self):
        if self.secondary_end_reading and self.secondary_start_reading:
            secondary_reading=(self.secondary_end_reading-self.secondary_start_reading)/24
            return secondary_reading
        else:
            return None
    def __str__(self):
        return str(self.batch_id)

    class Meta:
        verbose_name = "Hour Tracking"
        verbose_name_plural = "Hours Tracking"

    


class DayProduction(models.Model):
    batch_id = models.DateField(auto_now_add=True, unique=True)
    dust = models.FloatField(blank=True,  default=0.0)
    six_mm = models.FloatField(blank=True, default=0.0)
    twelve_mm = models.FloatField(blank=True, default=0.0)
    twenty_mm = models.FloatField(blank=True, default=0.0)
    forty_mm = models.FloatField(blank=True, default=0.0)
    sixty_mm = models.FloatField(blank=True, default=0.0)
    wetmix = models.FloatField(blank=True, default=0.0)
    gravel = models.FloatField(blank=True, default=0.0)
    gsb = models.FloatField(blank=True, default=0.0)
    remarks = models.TextField(null=True, blank=True)

    
    @property
    def day_out(self):
        if self.dust or self.six_mm or self.twelve_mm or self.twenty_mm or self.forty_mm or self.sixty_mm or self.wetmix or self.gravel or self.gsb:
            day_out=self.dust+self.six_mm+self.twelve_mm+self.twenty_mm+self.forty_mm+self.sixty_mm+self.wetmix+self.gravel+self.gsb
            return day_out
        else:
            return None
        
    def __str__(self):
        return str(self.batch_id)

    class Meta:
        verbose_name = "Day Production"
        verbose_name_plural = "Day Production"

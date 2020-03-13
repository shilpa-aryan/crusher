from django.contrib import admin

# Register your models here.
from crusher_app import models


admin.site.register(models.Driver)
admin.site.register(models.Vehicle)
admin.site.register(models.HoursTracking)
admin.site.register(models.Trip)
admin.site.register(models.DayProduction)


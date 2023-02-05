from django.contrib import admin

from .models import Vehicle

from .models import Ride

class VehicleAdmin(admin.ModelAdmin):
    fields = ['driver', 'vehicle_type','license_number','max_capacity','special_info']

class RideAdmin(admin.ModelAdmin):
    fields = [
        'owner',
        'driver',
        'require_arrival_time',
        'require_vehicle_type',
        'create_time',
        'destination',
        'passengers',
        'allow_sharer',
        'special_info',
        'ride_status'
    ]

admin.site.register(Vehicle, VehicleAdmin)

admin.site.register(Ride, RideAdmin)
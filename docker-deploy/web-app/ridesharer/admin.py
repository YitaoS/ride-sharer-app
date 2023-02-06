from django.contrib import admin

from .models import Vehicle

from .models import Ride,ShareAction

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
        'ride_status',
    ]

class ShareActionAdmin(admin.ModelAdmin):
    field = [
        'sharer',
        'shared_ride',
        'sharer_num'
    ]

admin.site.register(Vehicle, VehicleAdmin)

admin.site.register(Ride, RideAdmin)

admin.site.register(ShareAction, ShareActionAdmin)
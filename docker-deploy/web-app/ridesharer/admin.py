from django.contrib import admin

from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    fields = ['driver', 'vehicle_type','license_number','max_capacity','special_info']

admin.site.register(Vehicle, VehicleAdmin)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle,Ride
    
class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class updateUserForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

VEHICLE_TYPE = [
    ("S", "SUV"),
    ("M", "MiniBus"),
    ("B", "Baby Car"),
    ("N", "Normal Car")
]

class updateVehicleForm(forms.ModelForm):

    vehicle_type = forms.CharField(max_length=1, widget=forms.widgets.Select(choices=VEHICLE_TYPE))
    license_number = forms.CharField(max_length = 50)
    max_capacity = forms.IntegerField(initial = 1)
    special_info = forms.CharField(max_length = 100,required = False)
    class Meta:
        model = Vehicle
        fields = ['vehicle_type','license_number','max_capacity','special_info']

class updateRideForm(forms.ModelForm):    
    destination = forms.CharField(max_length=100)    
    require_arrival_time = forms.DateTimeField(help_text='Format: 2022-01-01 12:00')
    require_vehicle_type = forms.CharField(
        max_length=1, widget=forms.widgets.Select(choices=VEHICLE_TYPE),required = False)
    total_passengers = forms.IntegerField(initial=1)
    special_info = forms.CharField(max_length=400, required=False)
    allow_sharer = forms.BooleanField(initial=False, required=False)
    class Meta:
        model = Ride
        fields = ['require_arrival_time','destination','total_passengers','require_vehicle_type','allow_sharer','special_info']

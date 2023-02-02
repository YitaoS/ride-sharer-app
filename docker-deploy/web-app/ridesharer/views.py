from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone

from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from .forms import *
from .models import *
###############
#log in/out & register 
###############

def user_register(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,"Account was create for  "+username)
            return HttpResponseRedirect('login')
        messages.success(request,"Invalid email address!")
    return render(request, 'ridesharer/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('home')
        else:
            messages.info(request, 'Username or password is uncorrect')
    context = {}
    return render(request, 'ridesharer/login.html', context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('login')


###############
#user stuff
###############

@login_required(login_url='ridesharer:user_login')
def user_update(request):
    if request.method == 'POST':
        form = updateUserForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request,"email changed to "+ email)
            return HttpResponseRedirect('user_info')
    form = updateUserForm(instance = request.user)
    name = request.user.username
    context = {'form':form,'name':name}
    return  render(request, 'ridesharer/user_info.html',context)


@login_required(login_url='ridesharer:user_login')
def user_home(request):
    name = request.user.username
    context = {'name':name}
    return render(request, 'ridesharer/home.html',context)

class driver_register(CreateView):
    model = Vehicle
    fields = ['vehicle_type', 'license_number', 'max_capacity', 'special_info']
    template_name = 'ridesharer/driver_register.html'
    def form_valid(self, form):
        form.instance.driver= self.request.user
        return super().form_valid(form)


class ride_create(CreateView):
    model = Ride
    fields = [ 'require_arrival_time','destination','total_passengers','require_vehicle_type','allow_sharer','special_info']
    template_name = 'ridesharer/ride_create.html'

    def form_valid(self, form):
        form.instance.owner= self.request.user
        form.instance.driver= "To be assigned"
        form.instance.ride_status = RideStatus.OPEN
        return super().form_valid(form)

@login_required(login_url='ridesharer:user_login')
def ride_detail(request, ride_id):
    if request.method == 'POST':
        form = updateRideForm(request.POST, instance = Ride.objects.filter(id=ride_id)[0])
        if form.is_valid():
            form.save()
            messages.success(request,"Ride status has been updated !")
            context = {'form':form}
            render(request, 'ridesharer/ride_modify.html',context)
        else:
            messages.warning(request,"Invalid input !")
    ride = Ride.objects.filter(id=ride_id)[0]
   
    if ride.ride_status == RideStatus.OPEN: 
        form = updateRideForm(instance = ride)
        context ={'form':form}
        return render(request, 'ridesharer/ride_modify.html',context)
    context ={'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'total_passengers':ride.total_passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info}
    return  render(request, 'ridesharer/ride_detail.html',context)

# def user_update(request):
#     if request.method == 'POST':
#         form = updateUserForm(request.POST, instance = request.user)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             messages.success(request,"email changed to "+ email)
#             return HttpResponseRedirect('user_info')
#     form = updateUserForm(instance = request.user)
#     name = request.user.username
#     context = {'form':form,'name':name}
#     return  render(request, 'ridesharer/user_info.html',context)

@login_required(login_url='ridesharer:user_login')
def ride_list(request):
    allRides = request.user.ride.all()
    rides = allRides.filter().exclude(ride_status=RideStatus.FINISH)
    context = {
        'rides': rides,
    }
    return render(request, 'ridesharer/ride_info.html', context)

##to do
""" @login_re quired(login_url='ridesharer:user_login')
def ride_update(request):
    if request.method == 'POST':
        form = cre(request.POST, instance = request.user.vehicle)
        if form.is_valid():
            form.save()
            messages.success(request,"Vehicle status has been updated !")
            return HttpResponseRedirect('vehicle_info')
        else:
            messages.warning(request,"Capacity should be positive !")
    form = updateVehicleForm(instance = request.user.vehicle)
    context ={'form':form}
    return  render(request, 'ridesharer/vehicle_info.html',context) """
###############
###driver stuff
###############
@login_required(login_url='ridesharer:user_login')
def vehicle_update(request):
    try:
        if request.method == 'POST':
            form = updateVehicleForm(request.POST, instance = request.user.vehicle)
            if form.is_valid():
                form.save()
                messages.success(request,"Vehicle status has been updated !")
                return HttpResponseRedirect('vehicle_info')
            else:
                messages.warning(request,"Capacity should be positive !")
        form = updateVehicleForm(instance = request.user.vehicle)
        context ={'form':form}
        return  render(request, 'ridesharer/vehicle_info.html',context)
    except AttributeError:
        messages.info(request,"You haven't register as a driver !")
        return HttpResponseRedirect('driver_register')

@login_required(login_url='ridesharer:user_login')
def vehicle_delete(request):
    my_vehicle = request.user.vehicle
    my_vehicle.delete()
    messages.success(request,"Successfully remove vehicle infomation!")
    return HttpResponseRedirect('driver_register')



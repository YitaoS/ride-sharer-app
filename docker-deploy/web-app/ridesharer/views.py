from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q

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
    fields = [ 'require_arrival_time','destination','passengers','require_vehicle_type','allow_sharer','special_info']
    template_name = 'ridesharer/ride_create.html'

    def form_valid(self, form):
        form.instance.owner= self.request.user
        form.instance.driver= None
        form.instance.ride_status = RideStatus.OPEN
        return super().form_valid(form)

@login_required(login_url='ridesharer:user_login')
def ride_delete(request, ride_id):
    ride = Ride.objects.filter(id=ride_id)[0] 
    ride.delete()
    messages.success(request,"Successfully delete ride!")
    return HttpResponseRedirect(reverse('ridesharer:ride_list'))

@login_required(login_url='ridesharer:user_login')
def ride_detail(request, ride_id):
    user = request.user.username
    ride = Ride.objects.filter(id=ride_id)[0] 
    owner = ride.owner.username
    require_arrival_time = ride.require_arrival_time
    destination = ride.destination
    passengers = ride.passengers
    allow_sharer = ride.allow_sharer
    require_vehicle_type = ride.get_require_vehicle_type_display()
    if ride.ride_status != 'C':
        #owner
        #post
        if request.method == 'POST':
            form = updateRideForm(request.POST, instance = ride)
            context = {'form':form, 'ride':ride}
            if form.is_valid():
                form.save()
                messages.success(request,"Ride status has been updated !")
                render(request, 'ridesharer/ride_modify.html',context)
            else:
                messages.warning(request,"Invalid input !")
        #get
        if ride.sharing_actions.all():
            share_actions = ride.sharing_actions.all()
            context ={'owner':owner,'share_actions':share_actions,'driver':"",'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride.get_ride_status_display(),'user':user}
            return  render(request, 'ridesharer/ride_detail.html',context)
        form = updateRideForm(instance = ride)
        context ={'form':form, 'ride':ride}
        return render(request, 'ridesharer/ride_modify.html',context)
    if request.method == 'POST':
        ride.ride_status = 'F'
        ride.save()
        rides = request.user.driver_ride.all().filter(ride_status=RideStatus.CONFIRMED)
        context = {
            'rides': rides,
        }
        return render(request, 'ridesharer/ride_info.html', context)
    driver = ride.driver.username
    vehicle_type = ride.driver.vehicle.vehicle_type
    license_number = ride.driver.vehicle.license_number
    max_capacity = ride.driver.vehicle.max_capacity
    special_info = ride.driver.vehicle.special_info
    try:
        share_actions = ride.sharing_actions.all()
        context ={'owner':owner,'share_actions':share_actions,'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride.get_ride_status_display(),'vehicle_type': vehicle_type,'license_number': license_number,'max_capacity': max_capacity,'driver_special_info': special_info,'user':user}
        return  render(request, 'ridesharer/ride_detail.html',context)
    except AttributeError:
        context ={'owner':owner,'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride.get_ride_status_display(),'vehicle_type': vehicle_type,'license_number': license_number,'max_capacity': max_capacity,'driver_special_info': special_info,'user':user}
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

@login_required(login_url='ridesharer:user_login')
def joined_ride_list(request):
    allActions = request.user.share_actions.all()
    rides = []
    for action in allActions:
        if action.shared_ride.ride_status != 'F':
            rides.append(action.shared_ride)
    context = {
        'rides': rides,
    }
    return render(request, 'ridesharer/joined_ride_list.html', context)

def joined_ride_detail(request, ride_id):
    ride = Ride.objects.filter(id=ride_id)[0]
    driver = "To be assigned"
    if request.method == 'POST':
        allActions = request.user.share_actions.all()
        for action in allActions:
            if action.shared_ride.id == ride_id:
                action.shared_ride.passengers -= action.sharer_num
                action.shared_ride.save()
                action.delete()
            return HttpResponseRedirect(reverse('ridesharer:joined_ride_list'))
    share_actions = ride.sharing_actions.all()
    ride_status = ride.get_ride_status_display()
    if ride_status != 'confirmed':
        context ={'ride_status':ride_status,'share_actions':share_actions,'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display,'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride_status}
        return  render(request, 'ridesharer/joined_ride_detail.html',context)
    driver = ride.driver.username
    vehicle_type = ride.driver.vehicle.get_vehicle_type_display()
    license_number = ride.driver.vehicle.license_number
    max_capacity = ride.driver.vehicle.max_capacity
    special_info = ride.driver.vehicle.special_info
    context ={'ride_status':ride_status,'share_actions':share_actions,'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'my_special_info':ride.special_info,'vehicle_type': vehicle_type,'license_number': license_number,'max_capacity': max_capacity,'driver_special_info': special_info}
    return  render(request, 'ridesharer/joined_ride_detail.html',context)

@login_required(login_url='ridesharer:user_login')
def order_list(request):
    try: 
        request.user.vehicle
        allRides = request.user.driver_ride.all()
        rides = allRides.filter(ride_status=RideStatus.CONFIRMED)
        context = {
            'rides': rides,
        }
        return render(request, 'ridesharer/ride_info.html', context)
    except AttributeError:
        messages.info(request,"You haven't register as a driver !")
        return HttpResponseRedirect('driver_register')

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
    ride = Ride.objects.filter(driver=request.user,ride_status='C')
    if ride:
        messages.warning(request,"You still have ride order to complete!")
        return HttpResponseRedirect(reverse('ridesharer:vehicle_info'))
    else:
        my_vehicle = request.user.vehicle
        my_vehicle.delete()
        messages.success(request,"Successfully remove vehicle infomation!")
        return HttpResponseRedirect('driver_register')

@login_required(login_url='ridesharer:user_login')
def ride_confirm(request,ride_id):
    ride = Ride.objects.filter(id=ride_id)[0]
    if request.method == 'POST':
        ride.driver = request.user
        ride.ride_status = 'C'
        ride.save()
        receivers = []
        rider_email = get_object_or_404(User, id=ride.owner.id).email
        receivers.append(rider_email)
        allActions = ShareAction.objects.filter(shared_ride=ride)
        for action in allActions:
            sharer_email = action.sharer.email
            receivers.append(sharer_email)
        send_mail(
            'Driver Comfirmed Your Order',
            'Your ride order to' + ride.destination + 'is confirmed!',
            'chensuo568@gmail.com',
             receivers,
            fail_silently=False,
        )
        pass
    if ride.driver == None:
        driver = "To be assigned"
    else:
        driver = ride.driver.username
    context ={'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride.get_ride_status_display()}
    return  render(request, 'ridesharer/ride_confirm.html',context)

@login_required(login_url='ridesharer:user_login')
def confirm_join(request,ride_id,passengers_num):
    ride = Ride.objects.filter(id=ride_id)[0]
    driver = "To be assigned"
    if request.method == 'POST':
        share_action = ShareAction(sharer=request.user,shared_ride=ride,sharer_num=passengers_num)
        share_action.save()
        request.user.share_actions.add(share_action)
        ride.passengers += passengers_num
        ride.save()
        return HttpResponseRedirect(reverse('ridesharer:joined_ride_list'))
    try:
        share_actions = ride.sharing_actions.all()
        context ={'share_actions':share_actions,'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride.get_ride_status_display()}
        return  render(request, 'ridesharer/ride_join.html',context)
    except AttributeError:
        context ={'driver':driver,'require_arrival_time':ride.require_arrival_time,'destination':ride.destination,'passengers':ride.passengers,'require_vehicle_type':ride.get_require_vehicle_type_display(),'allow_sharer':ride.allow_sharer,'special_info':ride.special_info,'ride_status':ride.get_ride_status_display()}
        return  render(request, 'ridesharer/ride_join.html',context)

@login_required(login_url='ridesharer:user_login')
def search_rides_for_driver(request):
    try:        
        vehicle_profile = request.user.vehicle# access all available open rides for driver
        allRides = Ride.objects.filter(Q(passengers__lte=vehicle_profile.max_capacity)& ~Q(owner = request.user)& Q(ride_status = RideStatus.OPEN)& (Q(require_vehicle_type=vehicle_profile.vehicle_type) | Q(require_vehicle_type=''))& (Q(special_info=vehicle_profile.special_info)| Q(special_info='')))
        rides = []
        for ride in allRides:
            isSharer = False
            for action in request.user.share_actions.all():
                if action.shared_ride == ride:
                    isSharer = True
                    break
            if not isSharer:
                rides.append(ride)
                    
        context = {'rides':rides}
        return render(request, 'ridesharer/driver_ride_search.html', context)
    except AttributeError:
        messages.info(request,"You haven't register as a driver !")
        return HttpResponseRedirect('driver_register')

@login_required(login_url='ridesharer:user_login')
def search_rides_for_sharer(request):
    if request.method == 'POST':
        form = sharableOrderSearchCreateForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            earleist_arrival_time = form.cleaned_data['earleist_arrival_time']
            latetest_arrival_time = form.cleaned_data['latetest_arrival_time']
            passengers_num = form.cleaned_data['passengers_num']
            if earleist_arrival_time > latetest_arrival_time:
                messages.warning(request,"earleist_arrival_time should be before latetest_arrival_time!")
                form = sharableOrderSearchCreateForm()
                context ={'form':form}
                return  render(request, 'ridesharer/sharable_order_search.html',context)
            if passengers_num <= 0:
                messages.warning(request,"Passenger number should be positive !")
                form = sharableOrderSearchCreateForm()
                context ={'form':form}
                return  render(request, 'ridesharer/sharable_order_search.html',context)
            Allrides = Ride.objects.filter(~Q(owner = request.user)&Q(destination=destination)& Q(ride_status = RideStatus.OPEN)& Q(require_arrival_time__gte=earleist_arrival_time)& Q(require_arrival_time__lte=latetest_arrival_time)& Q(allow_sharer=True))
            rides = []
            for ride in Allrides:
                contain = False
                for action in request.user.share_actions.all():
                    if action.shared_ride == ride:
                        contain = True
                        break
                if contain == False:
                    rides.append(ride)
            context = {'rides':rides, 'user':request.user,'passengers_num':passengers_num}
            return render(request, 'ridesharer/sharable_ride_list.html', context)
        else:
            messages.warning(request,"Invalid form input!")
    form = sharableOrderSearchCreateForm()
    context ={'form':form}
    return  render(request, 'ridesharer/sharable_order_search.html',context)

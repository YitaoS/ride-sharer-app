from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'ridesharer'
urlpatterns = [
    #path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    path('home', views.user_home, name='user_home'),
    path('logout', views.user_logout, name='user_logout'),
    path('driver_register',login_required(views.driver_register.as_view()), name='driver_register'),
    path('vehicle_info', views.vehicle_update, name='vehicle_info'),
    path('vehicle_delete', views.vehicle_delete, name='vehicle_delete'),
    path('user_info', views.user_update, name='user_update'),
    path('ride_create', login_required(views.ride_create.as_view()), name='ride_create'),
    path('ride_list',  views.ride_list, name='ride_list'),
    path('joined_ride_list',  views.joined_ride_list, name='joined_ride_list'),
    path('joined_ride_detail/<int:ride_id>',  views.joined_ride_detail, name='joined_ride_detail'),
    path('<int:ride_id>/ride_delete',  views.ride_delete, name='ride_delete'),
    path('order_list',  views.order_list, name='order_list'),
    path('<int:ride_id>/', views.ride_detail, name='ride_detail'),
    path('<int:ride_id>/confirm', views.ride_confirm, name='ride_confirm'),
    path('search_rides_for_driver', views.search_rides_for_driver, name='search_rides_for_driver'),
    path('search_rides_for_sharer', views.search_rides_for_sharer, name='search_rides_for_sharer'),
    path('<int:ride_id>/<int:passengers_num>/confirm_join', views.confirm_join, name='confirm_join')
]
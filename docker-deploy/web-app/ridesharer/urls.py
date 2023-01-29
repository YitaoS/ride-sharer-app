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
    path('ride_create', login_required(views.ride_create.as_view()), name='ride_create')
]
from django.urls import path
from .. import views

urlpatterns = [
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]
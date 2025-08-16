from django.urls import path
from .. import views

urlpatterns = [
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
]
from django.urls import path
from .. import views

urlpatterns = [
    path('histories/', views.histories_list, name='histories_list'),
    path('histories/new/', views.history_create, name='history_create'),
    path('histories/<int:pk>/edit/', views.history_update, name='history_update'),
    path('histories/<int:pk>/delete/', views.history_delete, name='history_delete'),
]
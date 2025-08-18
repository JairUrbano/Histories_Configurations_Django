from django.urls import path
from .. import views

urlpatterns = [
    path('document-types/', views.document_types_list, name='document_types_list'),
    path('document-types/new/', views.document_type_create, name='document_type_create'),
    path('document-types/<int:pk>/edit/', views.document_type_update, name='document_type_update'),
    path('document-types/<int:pk>/delete/', views.document_type_delete, name='document_type_delete'),
]
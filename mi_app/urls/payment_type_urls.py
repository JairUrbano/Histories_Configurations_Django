from django.urls import path
from mi_app.views.payment_type_views import (
    payment_types_list,
    payment_type_create,
    payment_type_update,
    payment_type_delete
)

urlpatterns = [
    path('payment-types/', payment_types_list, name='payment_types_list'),
    path('payment-types/new/', payment_type_create, name='payment_type_create'),
    path('payment-types/<int:pk>/edit/', payment_type_update, name='payment_type_update'),
    path('payment-types/<int:pk>/delete/', payment_type_delete, name='payment_type_delete'),
]

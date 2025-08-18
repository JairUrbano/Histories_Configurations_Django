from django.urls import path
from .. import views

urlpatterns = [
    path('predetermined-prices/', views.predetermined_prices_list, name='predetermined_prices_list'),
    path('predetermined-prices/new/', views.predetermined_price_create, name='predetermined_price_create'),
    path('predetermined-prices/<int:pk>/edit/', views.predetermined_price_update, name='predetermined_price_update'),
    path('predetermined-prices/<int:pk>/delete/', views.predetermined_price_delete, name='predetermined_price_delete'),
]
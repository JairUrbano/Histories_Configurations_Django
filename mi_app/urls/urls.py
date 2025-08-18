from django.urls import path, include

urlpatterns = [
    path('', include('mi_app.urls.appointment_urls')),
    path('', include('mi_app.urls.document_type_urls')),
    path('', include('mi_app.urls.history_urls')),
    path('', include('mi_app.urls.patient_urls')),
    path('', include('mi_app.urls.payment_type_urls')),
    path('', include('mi_app.urls.predetermined_price_urls')),
]
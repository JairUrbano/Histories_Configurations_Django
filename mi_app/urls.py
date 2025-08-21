from django.urls import path
from .views.history import histories_list, history_create, history_update, history_delete
from .views.document_type import document_types_list, document_type_create, document_type_update, document_type_delete
from .views.payment_type import payment_types_list, payment_type_create, payment_type_update, payment_type_delete
from .views.predetermined_price import predetermined_prices_list, predetermined_price_create, predetermined_price_update, predetermined_price_delete

urlpatterns = [
    path("history/", histories_list, name="histories_list"),
    path("history/create/", history_create, name="history_create"),
    path("history/<int:id>/update/", history_update, name="history_update"),
    path("history/<int:id>/delete/", history_delete, name="history_delete"),

    path("document-type/", document_types_list, name="document_types_list"),
    path("document-type/create/", document_type_create, name="document_type_create"),
    path("document-type/<int:id>/update/", document_type_update, name="document_type_update"),
    path("document-type/<int:id>/delete/", document_type_delete, name="document_type_delete"),

    path("payment-type/", payment_types_list, name="payment_types_list"),
    path("payment-type/create/", payment_type_create, name="payment_type_create"),
    path("payment-type/<int:pk>/update/", payment_type_update, name="payment_type_update"),
    path("payment-type/<int:pk>/delete/", payment_type_delete, name="payment_type_delete"),

    path("predetermined-price/", predetermined_prices_list, name="predetermined_prices_list"),
    path("predetermined-price/create/", predetermined_price_create, name="predetermined_price_create"),
    path("predetermined-price/<int:pk>/update/", predetermined_price_update, name="predetermined_price_update"),
    path("predetermined-price/<int:pk>/delete/", predetermined_price_delete, name="predetermined_price_delete"),
]

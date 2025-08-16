from django.db import models
from .payment_type import PaymentType
from .predetermined_price import PredeterminedPrice

class Appointment(models.Model):
    payment_type = models.ForeignKey(PaymentType, related_name="appointments", on_delete=models.CASCADE)
    predetermined_price = models.ForeignKey(
        PredeterminedPrice,
        related_name="appointments",
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    date = models.DateTimeField()
    description = models.TextField(
        blank=True, null=True,
        error_messages={'max_length': 'La descripción no debe superar los 1000 caracteres.'}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "appointments"

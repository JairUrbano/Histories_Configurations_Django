from django.db import models
from django.utils import timezone

# Manager para devolver solo objetos no eliminados
class ActivePaymentTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class PaymentType(models.Model):
    code = models.CharField(
        max_length=50,
        error_messages={'max_length': 'El código no debe superar los 50 caracteres.'}
    )
    name = models.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Manager que solo devuelve registros activos
    objects = ActivePaymentTypeManager()

    # Métodos para soft delete y restaurar
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "payment_types"

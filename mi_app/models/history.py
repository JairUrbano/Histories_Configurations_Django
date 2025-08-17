from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .patient import Patient


class ActiveHistoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class History(models.Model):
    testimony = models.TextField(blank=True, null=True)
    private_observation = models.TextField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    last_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    menstruation = models.BooleanField(default=False)
    diu_type = models.CharField(
        max_length=255,
        blank=True, null=True,
        error_messages={'max_length': 'El tipo de DIU no debe superar los 255 caracteres.'}
    )
    gestation = models.BooleanField(default=False)

    patient = models.ForeignKey(Patient, related_name="histories", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = ActiveHistoryManager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        existe_activo = History.objects.filter(
            patient=self.patient,
            deleted_at__isnull=True
        ).exclude(pk=self.pk).exists()
        if existe_activo:
            raise ValueError("El paciente ya tiene un historial activo. No se puede restaurar.")
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"History (Paciente: {self.patient.id}, Fecha: {self.created_at.date()})"

    class Meta:
        db_table = "histories"
        constraints = [
            models.UniqueConstraint(
                fields=['patient'],
                condition=models.Q(deleted_at__isnull=True),
                name='unique_active_history_per_patient'
            )
        ]

from django.db import models
from .document_type import DocumentType

class Patient(models.Model):
    name = models.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True)
    document_number = models.CharField(
        max_length=50,
        blank=True, null=True,
        error_messages={'max_length': 'El número de documento no debe superar los 50 caracteres.'}
    )
    birth_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "patients"

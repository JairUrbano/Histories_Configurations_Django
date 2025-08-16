from django import forms
from ..models import Patient

class PatientForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )
    document_number = forms.CharField(
        required=False,
        max_length=50,
        error_messages={'max_length': 'El número de documento no debe superar los 50 caracteres.'}
    )

    class Meta:
        model = Patient
        fields = ['name', 'document_type', 'document_number', 'birth_date']

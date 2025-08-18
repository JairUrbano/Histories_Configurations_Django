from django import forms
from ..models import Appointment

class AppointmentForm(forms.ModelForm):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        max_length=1000,
        error_messages={'max_length': 'La descripción no debe superar los 1000 caracteres.'}
    )

    class Meta:
        model = Appointment
        fields = [
            'payment_type',
            'predetermined_price',
            'date',
            'description'
        ]

    def clean_date(self):
        date = self.cleaned_data.get('date')
        return date

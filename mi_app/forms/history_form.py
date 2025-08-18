from django import forms
from ..models import History

class HistoryForm(forms.ModelForm):
    diu_type = forms.CharField(
        required=False,
        max_length=255,
        error_messages={'max_length': 'El tipo de DIU no debe superar los 255 caracteres.'}
    )

    class Meta:
        model = History
        fields = [
            'testimony', 'private_observation', 'observation',
            'height', 'weight', 'last_weight',
            'menstruation', 'diu_type', 'gestation', 'patient'
        ]

    def clean_patient(self):
        patient = self.cleaned_data.get('patient')
        if not self.instance.pk:
            qs = History.objects.filter(patient=patient, deleted_at__isnull=True)
            if qs.exists():
                raise forms.ValidationError("Este paciente ya tiene un historial activo.")
        return patient

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            cambios = any(
                getattr(self.instance, campo) != valor
                for campo, valor in cleaned_data.items()
            )
            if not cambios:
                raise forms.ValidationError("No hubo cambios en el historial.")
        return cleaned_data

    def save(self, commit=True):
        patient = self.cleaned_data.get('patient')
        if not self.instance.pk:
            historial_eliminado = History.objects.filter(
                patient=patient,
                deleted_at__isnull=False
            ).first()
            if historial_eliminado:
                for campo, valor in self.cleaned_data.items():
                    setattr(historial_eliminado, campo, valor)
                historial_eliminado.deleted_at = None
                if commit:
                    historial_eliminado.save()
                return historial_eliminado
        return super().save(commit)

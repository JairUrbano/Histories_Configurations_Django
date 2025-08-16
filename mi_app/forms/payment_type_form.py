from django import forms
from ..models import PaymentType

class PaymentTypeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )
    code = forms.CharField(
        max_length=50,
        error_messages={'max_length': 'El código no debe superar los 50 caracteres.'}
    )

    class Meta:
        model = PaymentType
        fields = ['code', 'name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = PaymentType.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El tipo de pago ya está registrado.')
        return name

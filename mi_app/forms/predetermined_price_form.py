from django import forms
from ..models import PredeterminedPrice

class PredeterminedPriceForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )

    class Meta:
        model = PredeterminedPrice
        fields = ['name', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = PredeterminedPrice.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El precio predeterminado ya está registrado.')
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return price

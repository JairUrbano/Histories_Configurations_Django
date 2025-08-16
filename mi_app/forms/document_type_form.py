from django import forms
from ..models import DocumentType

class DocumentTypeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        error_messages={'max_length': 'El nombre no debe superar los 255 caracteres.'}
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        max_length=1000,
        error_messages={'max_length': 'La descripción no debe superar los 1000 caracteres.'}
    )

    class Meta:
        model = DocumentType
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = DocumentType.objects.filter(name=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('El tipo de documento ya está registrado.')
        return name

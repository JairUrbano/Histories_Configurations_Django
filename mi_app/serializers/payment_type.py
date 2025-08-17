
from rest_framework import serializers
from mi_app.models.patient import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    def validate_document_number(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("El número de documento debe tener al menos 5 caracteres.")
        return value

    def validate_birth_date(self, value):
        from datetime import date
        if value and value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value

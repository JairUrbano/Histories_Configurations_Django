from rest_framework import serializers
from mi_app.models.patient import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_document_number(self, value):
        if value and len(value) > 50:
            raise serializers.ValidationError("El número de documento no debe superar los 50 caracteres.")
        return value

    def validate(self, data):
        # Ejemplo: si hay documento, debe tener tipo
        if data.get('document_number') and not data.get('document_type'):
            raise serializers.ValidationError("Si se ingresa un número de documento, debe seleccionar un tipo de documento.")
        return data

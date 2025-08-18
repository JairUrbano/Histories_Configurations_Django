from rest_framework import serializers
from mi_app.models.appointment import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_description(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError("La descripción no debe superar los 1000 caracteres.")
        return value

    def validate_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("La fecha de la cita no puede ser pasada.")
        return value

    def validate(self, data):
        # Validación cruzada: si hay precio predeterminado, debe existir un payment_type
        if data.get('predetermined_price') and not data.get('payment_type'):
            raise serializers.ValidationError(
                "Si se define un precio predeterminado, debe seleccionarse un tipo de pago."
            )
        return data

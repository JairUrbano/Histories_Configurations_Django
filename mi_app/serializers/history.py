from rest_framework import serializers
from mi_app.models.history import History

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    def validate_height(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("La altura debe ser mayor a 0.")
        return value

    def validate_weight(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("El peso debe ser mayor a 0.")
        return value

    def validate(self, data):
        # Validación cruzada: no puede estar gestando y menstruando a la vez
        if data.get('gestation') and data.get('menstruation'):
            raise serializers.ValidationError(
                "No puede estar en gestación y menstruación al mismo tiempo."
            )
        return data

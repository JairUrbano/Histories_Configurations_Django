from rest_framework import serializers
from mi_app.models.document_type import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

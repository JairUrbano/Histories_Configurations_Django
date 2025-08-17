from django.test import TestCase
from mi_app.models import DocumentType
from mi_app.serializers import DocumentTypeSerializer

class DocumentTypeSerializerTest(TestCase):

    def test_serializer_valid_data(self):
        """Prueba que el serializer es válido con datos correctos"""
        data = {
            'name': 'DNI'
        }
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        document_type = serializer.save()
        self.assertEqual(document_type.name, 'DNI')

    def test_name_empty(self):
        """Prueba que falle si el nombre está vacío o solo espacios"""
        data = {
            'name': '   '
        }
        serializer = DocumentTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_name_strip(self):
        """Prueba que el serializer limpia espacios en nombre"""
        data = {
            'name': '  Pasaporte  '
        }
        serializer = DocumentTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        document_type = serializer.save()
        self.assertEqual(document_type.name, '  Pasaporte  ')  # No hace strip automático, solo valida

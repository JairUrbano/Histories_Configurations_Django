from django.test import TestCase
from mi_app.models import Patient, DocumentType
from mi_app.serializers import PatientSerializer
from django.utils import timezone

class PatientSerializerTest(TestCase):

    def setUp(self):
        # Crear un DocumentType para relacionarlo con Patient
        self.doc_type = DocumentType.objects.create(name="DNI")

    def test_serializer_valid_data(self):
        """Prueba que el serializer es válido con datos correctos"""
        data = {
            'name': 'Juan Pérez',
            'document_type': self.doc_type.id,
            'document_number': '12345678',
            'birth_date': '1990-01-01'
        }
        serializer = PatientSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        patient = serializer.save()
        self.assertEqual(patient.name, 'Juan Pérez')
        self.assertEqual(patient.document_number, '12345678')

    def test_name_empty(self):
        """Prueba que falle si el nombre está vacío o solo espacios"""
        data = {
            'name': '   ',
            'document_type': self.doc_type.id,
            'document_number': '12345678'
        }
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_document_number_too_long(self):
        """Prueba que falle si el número de documento supera 50 caracteres"""
        data = {
            'name': 'Ana',
            'document_type': self.doc_type.id,
            'document_number': 'a' * 51
        }
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('document_number', serializer.errors)

    def test_document_number_without_type(self):
        """Prueba validación cruzada: número de documento sin tipo"""
        data = {
            'name': 'Carlos',
            'document_number': '98765432'
        }
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
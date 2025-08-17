from django.test import TestCase
from mi_app.models import Patient, DocumentType
from mi_app.serializers import PatientSerializer
from datetime import date, timedelta

class PatientSerializerTest(TestCase):

    def setUp(self):
        # Crear un DocumentType para la relación
        self.doc_type = DocumentType.objects.create(name="DNI")

    def test_serializer_valid_data(self):
        """Prueba que el serializer es válido con datos correctos"""
        data = {
            'name': 'Juan Pérez',
            'document_type': self.doc_type.id,
            'document_number': '12345',
            'birth_date': date(1990, 1, 1)
        }
        serializer = PatientSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        patient = serializer.save()
        self.assertEqual(patient.document_number, '12345')
        self.assertEqual(patient.birth_date, date(1990, 1, 1))

    def test_document_number_too_short(self):
        """Prueba que falle si el número de documento tiene menos de 5 caracteres"""
        data = {
            'name': 'Ana',
            'document_type': self.doc_type.id,
            'document_number': '1234',
            'birth_date': date(1990, 1, 1)
        }
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('document_number', serializer.errors)

    def test_birth_date_in_future(self):
        """Prueba que falle si la fecha de nacimiento es futura"""
        future_date = date.today() + timedelta(days=1)
        data = {
            'name': 'Carlos',
            'document_type': self.doc_type.id,
            'document_number': '12345',
            'birth_date': future_date
        }
        serializer = PatientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('birth_date', serializer.errors)
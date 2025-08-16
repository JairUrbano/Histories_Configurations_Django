from django.test import TestCase
from ..models import DocumentType, Patient
from ..forms import PatientForm

# -------------------------
# TESTS DE MODELO
# -------------------------
class PatientModelTest(TestCase):
    def setUp(self):
        self.doc_type = DocumentType.objects.create(name="DNI")

    def test_create_patient(self):
        patient = Patient.objects.create(
            name="Juan Perez",
            document_type=self.doc_type,
            document_number="12345678",
            birth_date="1990-01-01"
        )
        self.assertEqual(patient.name, "Juan Perez")
        self.assertEqual(patient.document_type, self.doc_type)
        self.assertIsNotNone(patient.id)

# -------------------------
# TESTS DE FORMULARIO
# -------------------------
class PatientFormTest(TestCase):
    def setUp(self):
        self.doc_type = DocumentType.objects.create(name='DNI')

    def test_valid_data(self):
        form = PatientForm(data={
            'name': 'Juan Perez',
            'document_type': self.doc_type.id,
            'document_number': '12345678',
            'birth_date': '1990-01-01'
        })
        self.assertTrue(form.is_valid())

    def test_name_length_limit(self): 
        form = PatientForm(data={
            'name': 'x' * 256,
            'document_type': self.doc_type.id,
            'document_number': '123',
            'birth_date': '1990-01-01'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('El nombre no debe superar los 255 caracteres.', form.errors['name'])
from django.test import TestCase
from ..models import DocumentType
from ..forms import DocumentTypeForm

# -------------------------
# TESTS DE MODELO
# -------------------------
class DocumentTypeModelTest(TestCase):
    def test_create_document_type(self):
        doc_type = DocumentType.objects.create(name="DNI", description="Documento nacional")
        self.assertEqual(doc_type.name, "DNI")
        self.assertEqual(doc_type.description, "Documento nacional")
        self.assertIsNotNone(doc_type.id)

# -------------------------
# TESTS DE FORMULARIO
# -------------------------
class DocumentTypeFormTest(TestCase):
    def test_valid_data(self):
        form = DocumentTypeForm(data={
            'name': 'DNI',
            'description': 'Documento Nacional de Identidad'
        })
        self.assertTrue(form.is_valid())

    def test_duplicate_name(self):
        DocumentType.objects.create(name='DNI')
        form = DocumentTypeForm(data={'name': 'DNI', 'description': 'Otro'})
        self.assertFalse(form.is_valid())
        self.assertIn('El tipo de documento ya está registrado.', form.errors['name'])
 
    def test_name_length_limit(self):
        form = DocumentTypeForm(data={'name': 'a' * 256})
        self.assertFalse(form.is_valid())
        self.assertIn('El nombre no debe superar los 255 caracteres.', form.errors['name'])
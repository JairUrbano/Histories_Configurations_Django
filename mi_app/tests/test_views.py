from django.test import TestCase
from django.urls import reverse
from ..models import DocumentType, Patient, PaymentType, PredeterminedPrice, History, Appointment

# -------------------------
# TESTS DE VISTAS
# -------------------------
class ViewsTest(TestCase):
    def setUp(self):
        self.doc_type = DocumentType.objects.create(name="DNI")
        self.patient = Patient.objects.create(name="Juan Perez", document_type=self.doc_type)
        self.payment_type = PaymentType.objects.create(code='EF', name='Efectivo')
        self.price = PredeterminedPrice.objects.create(name='Consulta', price=50.00)

        self.history = History.objects.create(patient=self.patient)
        self.appointment = Appointment.objects.create(
            payment_type=self.payment_type,
            predetermined_price=self.price,
            date="2025-12-31 10:00:00"
        )

    def test_document_types_list_view(self):
        response = self.client.get(reverse('document_types_list'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, self.doc_type.name)

    def test_document_type_create_view(self):
        response = self.client.post(reverse('document_type_create'), {
            'name': 'Carnet Ext',
            'description': 'Carnet de extranjería'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(DocumentType.objects.filter(name='Carnet Ext').exists())

    def test_patients_list_view(self):
        response = self.client.get(reverse('patients_list'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, self.patient.name)

    def test_patient_create_view(self):
        response = self.client.post(reverse('patient_create'), {
            'name': 'Maria Lopez',
            'document_type': self.doc_type.id,
            'document_number': '87654321',
            'birth_date': '1985-05-05'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Patient.objects.filter(name='Maria Lopez').exists())
from django.test import TestCase
from ..models import PaymentType, PredeterminedPrice
from ..forms import AppointmentForm

# -------------------------
# TESTS DE FORMULARIO
# -------------------------
class AppointmentFormTest(TestCase):
    def setUp(self):
        self.payment_type = PaymentType.objects.create(code='EF', name='Efectivo')
        self.price = PredeterminedPrice.objects.create(name='Consulta', price=50.00)

    def test_valid_data(self):
        form = AppointmentForm(data={
            'payment_type': self.payment_type.id,
            'predetermined_price': self.price.id,
            'date': '2025-12-31 10:00:00',
            'description': 'Consulta médica'
        })
        self.assertTrue(form.is_valid())

    def test_description_length_limit(self):
        form = AppointmentForm(data={
            'payment_type': self.payment_type.id,
            'predetermined_price': self.price.id,
            'date': '2025-12-31 10:00:00',
            'description': 'x' * 1001
        })
        self.assertFalse(form.is_valid())
        self.assertIn('La descripción no debe superar los 1000 caracteres.', form.errors['description'])
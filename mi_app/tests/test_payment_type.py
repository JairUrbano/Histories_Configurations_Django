from django.test import TestCase
from ..models import PaymentType
from ..forms import PaymentTypeForm

# -------------------------
# TESTS DE FORMULARIO
# -------------------------
class PaymentTypeFormTest(TestCase):
    def test_valid_data(self):
        form = PaymentTypeForm(data={
            'code': 'EF',
            'name': 'Efectivo'
        })
        self.assertTrue(form.is_valid())

    def test_duplicate_name(self):
        PaymentType.objects.create(code='EF', name='Efectivo')
        form = PaymentTypeForm(data={'code': 'EF2', 'name': 'Efectivo'})
        self.assertFalse(form.is_valid())
        self.assertIn('El tipo de pago ya está registrado.', form.errors['name'])
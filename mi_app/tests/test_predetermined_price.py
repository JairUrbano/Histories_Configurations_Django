from django.test import TestCase
from ..forms import PredeterminedPriceForm

# -------------------------
# TESTS DE FORMULARIO
# -------------------------
class PredeterminedPriceFormTest(TestCase):
    def test_valid_data(self):
        form = PredeterminedPriceForm(data={
            'name': 'Consulta General',
            'price': '50.00'
        })
        self.assertTrue(form.is_valid())

    def test_price_negative(self):
        form = PredeterminedPriceForm(data={
            'name': 'Consulta',
            'price': '-5.00'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('El precio no puede ser negativo.', form.errors['price'])
from django.test import TestCase
from mi_app.models import PredeterminedPrice
from mi_app.serializers import PredeterminedPriceSerializer

class PredeterminedPriceSerializerTest(TestCase):

    def test_serializer_valid_data(self):
        """Prueba que el serializer es válido con datos correctos"""
        data = {
            'name': 'Consulta General',
            'amount': 150.0
        }
        serializer = PredeterminedPriceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        price = serializer.save()
        self.assertEqual(price.name, 'Consulta General')
        self.assertEqual(price.amount, 150.0)

    def test_fields_included(self):
        """Verifica que los campos incluidos en el serializer sean correctos"""
        price = PredeterminedPrice.objects.create(name='Examen', amount=200.0)
        serializer = PredeterminedPriceSerializer(price)
        self.assertIn('id', serializer.data)
        self.assertIn('name', serializer.data)
        self.assertIn('amount', serializer.data)
        self.assertIn('created_at', serializer.data)
        self.assertIn('updated_at', serializer.data)
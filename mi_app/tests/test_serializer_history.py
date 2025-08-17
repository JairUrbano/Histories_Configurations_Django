from django.test import TestCase
from mi_app.models import History
from mi_app.serializers import HistorySerializer
from django.utils import timezone

class HistorySerializerTest(TestCase):

    def test_serializer_valid_data(self):
        """Prueba que el serializer es válido con datos correctos"""
        data = {
            'height': 170,
            'weight': 65,
            'gestation': False,
            'menstruation': True,
            'date': timezone.now()
        }
        serializer = HistorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        history = serializer.save()
        self.assertEqual(history.height, 170)
        self.assertEqual(history.weight, 65)

    def test_height_invalid(self):
        """Prueba que falle si la altura es 0 o negativa"""
        data = {
            'height': 0,
            'weight': 65,
            'gestation': False,
            'menstruation': True,
            'date': timezone.now()
        }
        serializer = HistorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('height', serializer.errors)

    def test_weight_invalid(self):
        """Prueba que falle si el peso es 0 o negativo"""
        data = {
            'height': 170,
            'weight': 0,
            'gestation': False,
            'menstruation': True,
            'date': timezone.now()
        }
        serializer = HistorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('weight', serializer.errors)

    def test_gestation_and_menstruation(self):
        """Prueba validación cruzada: no puede estar gestando y menstruando"""
        data = {
            'height': 170,
            'weight': 65,
            'gestation': True,
            'menstruation': True,
            'date': timezone.now()
        }
        serializer = HistorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
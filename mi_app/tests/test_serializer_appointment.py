from django.test import TestCase
from django.utils import timezone
from mi_app.models import Appointment, PaymentType, PredeterminedPrice
from mi_app.serializers import AppointmentSerializer
from datetime import timedelta

class AppointmentSerializerTest(TestCase):

    def setUp(self):
        # Crear objetos necesarios para relaciones
        self.payment_type = PaymentType.objects.create(name="Efectivo")
        self.price = PredeterminedPrice.objects.create(amount=100)

    def test_serializer_valid_data(self):
        """Prueba que el serializer es válido con datos correctos"""
        data = {
            'payment_type': self.payment_type.id,
            'predetermined_price': self.price.id,
            'date': timezone.now() + timedelta(days=1),
            'description': 'Cita de prueba'
        }
        serializer = AppointmentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        appointment = serializer.save()
        self.assertEqual(appointment.description, 'Cita de prueba')

    def test_description_too_long(self):
        """Prueba que falle si la descripción excede 1000 caracteres"""
        data = {
            'payment_type': self.payment_type.id,
            'date': timezone.now() + timedelta(days=1),
            'description': 'a' * 1001
        }
        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('description', serializer.errors)

    def test_date_in_past(self):
        """Prueba que falle si la fecha es pasada"""
        data = {
            'payment_type': self.payment_type.id,
            'date': timezone.now() - timedelta(days=1),
            'description': 'Cita pasada'
        }
        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date', serializer.errors)

    def test_cross_validation_price_without_payment(self):
        """Prueba validación cruzada: price sin payment_type"""
        data = {
            'predetermined_price': self.price.id,
            'date': timezone.now() + timedelta(days=1),
            'description': 'Cita con precio pero sin pago'
        }
        serializer = AppointmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

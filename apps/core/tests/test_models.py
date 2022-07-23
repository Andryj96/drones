from django.test import TestCase
from apps.core.models import Drone, Medication


class DroneTest(TestCase):

    def create_drone(self, serial_no='AdS-21', model='Lightweight', weight_limit=100, battery=100, state='IDLE'):
        return Drone.objects.create(
            serial_no=serial_no,
            model=model,
            weight_limit=weight_limit,
            battery=battery,
            state=state
        )

    def test_drone_creation(self):
        drone = self.create_drone()
        self.assertTrue(isinstance(drone, Drone))
        self.assertEqual(str(drone), 'Lightweight - AdS-21')


class MedicationTest(TestCase):

    def create_medication(self, name='Aspirin', weight=50, code='ASP'):
        return Medication.objects.create(
            name=name,
            weight=weight,
            code=code,
        )

    def test_medication_creation(self):
        medication = self.create_medication()
        self.assertIsInstance(medication, Medication)
        self.assertEqual(str(medication), 'Aspirin')

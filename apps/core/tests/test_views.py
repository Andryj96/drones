from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.core.models import Drone, Medication
from django.contrib.auth import get_user_model

User = get_user_model()


class DroneTest(APITestCase):
    def test_create_drone(self):
        """
        Ensure we can create a new drone object.
        """
        url = reverse('drones-list')
        data = {'serial_no': 'AFS-012', 'model': 'Lightweight',
                'weight_limit': 100, 'battery': 100, 'state': 'IDLE'}

        user = User.objects.create(
            username='user',
            email='user@gmail.com',
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(
            url,
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.count(), 1)
        self.assertEqual(Drone.objects.get().serial_no, 'AFS-012')

        data = {'serial_no': 'AFS_012', 'model': 'Lightweight',
                'weight_limit': 700, 'battery': 100, 'state': 'IDLE'}

        response = self.client.post(
            url,
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MedicationTest(APITestCase):
    def test_create_medication(self):
        """
        Ensure we can create a new medication object.
        """
        url = reverse('medication-list')
        data = {'name': 'Aspirin', 'weight': 50, 'code': 'ASP'}

        user = User.objects.create(
            username='user',
            email='user@gmail.com',
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(
            url,
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medication.objects.count(), 1)
        self.assertEqual(Medication.objects.get().code, 'ASP')

        data = {'name': 'Aspirin', 'weight': 50, 'code': 'ASP-1'}

        response = self.client.post(
            url,
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.core.models import Drone, LoadedMedication, Medication
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


class DroneLoadingTest(APITestCase):
    def create_drones(self):
        drone1 = Drone.objects.create(
            serial_no='AFS-012',
            model='Lightweight',
            weight_limit=400,
            battery=100,
            state='IDLE'
        )
        drone2 = Drone.objects.create(
            serial_no='AFS-013',
            model='Lightweight',
            weight_limit=400,
            battery=22,
            state='IDLE'
        )
        return [drone1, drone2]

    def create_user(self):
        return User.objects.create(
            username='user',
            email='user@gmail.com',
        )

    def create_medication(self):
        return Medication.objects.create(
            name='Aspirin',
            weight=50,
            code='ASP-1',
        )

    def test_create_drone_loading(self):
        """
        Ensure we can load a drone with medication items.
        """
        url = reverse('loadedmedication-list')

        self.drones = self.create_drones()

        self.medication = self.create_medication()

        data = {'drone': self.drones[0].uuid,
                'medications': [self.medication.uuid]}

        self.user = self.create_user()

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            url,
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoadedMedication.objects.count(), 1)
        self.assertEqual(LoadedMedication.objects.get().drone, self.drones[0])

        # Create load with battery low drone

        data = {'drone': self.drones[1].uuid,
                'medications': [self.medication.uuid]}

        response = self.client.post(
            url,
            data,
            format='json',
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         response.json())

        # check loaded medication

        url = reverse(
            'loaded-medications',
            kwargs={'uuid': self.drones[0].uuid}
        )
        response = self.client.get(
            url,
            data,
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.json()
        )
        self.assertEqual(
            LoadedMedication.objects.count(),
            response.json()['count'],
        )

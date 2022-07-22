from rest_framework import viewsets, generics, response, views
from apps.core import models, serializers
from apps.core.utils import is_valid_uuid
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from drones.celery import debug_task


class Drones(generics.ListCreateAPIView, viewsets.GenericViewSet):
    """
    List all drones, or create a new drone.
    """
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['serial_no', 'model', 'state']


class DroneDetail(generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    """
    Retrieve, update or delete a drone instance.
    """
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer
    lookup_field = 'uuid'


class AvailableDrones(generics.ListAPIView, viewsets.GenericViewSet):
    """
    List all available drones (considere as available the IDLE stete and battery status up or equal to 25%).
    """
    queryset = models.Drone.objects.filter(
        state=models.DRONE_STATUS.IDLE,
        battery__gte=25
    )
    serializer_class = serializers.DroneSerializer


class GetDroneBatteryLevel(views.APIView):
    """
    Get the battery level of a drone.
    """

    def get(self, request, uuid):
        try:
            drone = models.Drone.objects.values('battery').get(uuid=uuid)
        except Exception:
            return response.Response(status=404)

        return response.Response({'battery': drone['battery']})


class Medications(viewsets.ModelViewSet):
    """
    List, create, retrieve, update or destroy medications.
    """
    queryset = models.Medication.objects.all()
    serializer_class = serializers.MedicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code', 'name']
    lookup_field = 'uuid'


class DroneLoading(generics.CreateAPIView, viewsets.GenericViewSet):
    """
    Loading a drone with medication items.

    The drone must be in IDLE state and battery level up or equal to 25%.
    and the total weight of the medication items must be less than the drone weight limit.

    There are no medications loaded without delivery for this drone (Consider field `delivered`
    in LoadedMedication Model checked when the load was delivered).
    """
    queryset = models.LoadedMedication.objects.all()
    serializer_class = serializers.DroneLoadingSerializer


class LoadedMedications(generics.ListAPIView, viewsets.GenericViewSet):
    """
    List all loaded medications for a given drone .
    """
    queryset = models.LoadedMedication.objects.all()
    serializer_class = serializers.DroneLoadingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['delivered', ]

    def get_queryset(self):
        qs = super().get_queryset()

        drone_uuid = self.kwargs['uuid'] if is_valid_uuid(
            self.kwargs['uuid']) else None

        qs = qs.filter(
            drone__uuid=drone_uuid
        )

        return qs


@api_view()
def celery_test_view(request):
    debug_task.delay()
    return response.Response({"message": "Your task is being processed!"})


class DroneLogs(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Battery level History for all drones.

    """
    queryset = models.DroneLog.objects.all()
    serializer_class = serializers.DroneLogSerializer
    filter_backends = [DjangoFilterBackend]
    filerset_fields = {
        'drone__uuid': ['exact'],
        'updated_at': ['gte', 'lte'],
    }

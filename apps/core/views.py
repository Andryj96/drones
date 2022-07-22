from rest_framework import viewsets, generics, response, views
from apps.core import models, serializers


class Drones(generics.ListCreateAPIView, viewsets.GenericViewSet):
    """
    List all drones, or create a new drone.
    """
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer


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

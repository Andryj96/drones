from rest_framework import viewsets, generics
from apps.core import models, serializers


class Drones(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = models.Drone.objects.all()
    serializer_class = serializers.DroneSerializer

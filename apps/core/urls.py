from django.urls import include, path
from rest_framework import routers
from apps.core import views
router = routers.DefaultRouter()

router.register(r'drones/list', views.Drones)
router.register(r'drones/detail', views.DroneDetail)
router.register(r'drones/available', views.AvailableDrones)
router.register(r'drones/load', views.DroneLoading)
router.register(r'medications/list', views.Medications)

urlpatterns = [
    path('', include(router.urls)),
    path('drones/battery/<uuid>/', views.GetDroneBatteryLevel.as_view()),
]

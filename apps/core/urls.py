from django.urls import include, path
from rest_framework import routers
from apps.core import views
router = routers.DefaultRouter()

router.register(r'drones/list', views.Drones, basename='drones')
router.register(r'drones/detail', views.DroneDetail)
router.register(r'drones/available', views.AvailableDrones,
                basename='available-drones')
router.register(r'drones/load', views.DroneLoading)
router.register(r'drones/log', views.DroneLogs)
router.register(r'medications/list', views.Medications)

urlpatterns = [
    path('', include(router.urls)),
    path('drones/battery/<uuid>/', views.GetDroneBatteryLevel.as_view(),
         name='get-drone-battery'),
    path('medications/loaded/<uuid>/',
         views.LoadedMedications.as_view({'get': 'list'}),
         name='loaded-medications',
         ),
    path('celery-test', views.celery_test_view, name='celery-test'),
]

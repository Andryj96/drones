from django.urls import include, path
from rest_framework import routers
from apps.core import views
router = routers.DefaultRouter()

router.register(r'drones', views.Drones)

urlpatterns = [
    path('', include(router.urls)),
]

from django.contrib import admin
from apps.core import models


admin.site.register(models.Drone)
admin.site.register(models.DroneLog)
admin.site.register(models.Medication)
admin.site.register(models.LoadedMedication)

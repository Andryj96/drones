from celery import shared_task
from .models import Drone, DroneLog
from django.utils import timezone


@shared_task
def check_drone_battery_log():
    for drone in Drone.objects.iterator():
        drone_log, created = DroneLog.objects.get_or_create(drone=drone)

        drone_log.history.append(
            dict(
                baterry=drone.battery,
                datetime=timezone.now(),
                state=drone.state,
            )
        )

        drone_log.save()

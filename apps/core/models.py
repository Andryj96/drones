from django.core.serializers.json import DjangoJSONEncoder
from email.policy import default
import uuid
from django.db import models
from django.core.validators import MaxValueValidator


class GenericModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.uuid)


class MODEL_TYPE(models.TextChoices):
    LIGHTWEIGHT = 'Lightweight', 'Lightweight'
    MIDDLEWEIGHT = 'Middleweight', 'Middleweight'
    CRUISERWEIGHT = 'Cruiserweight', 'Cruiserweight'
    HEAVYWEIGHT = 'Heavyweight', 'Heavyweight'


class DRONE_STATUS(models.TextChoices):
    IDLE = 'IDLE', 'IDLE'
    LOADING = 'LOADING', 'LOADING'
    LOADED = 'LOADED', 'LOADED'
    DELIVERING = 'DELIVERING', 'DELIVERING'
    DELIVERED = 'DELIVERED', 'DELIVERED'
    RETURNING = 'RETURNING', 'RETURNING'


class Drone(GenericModel):
    serial_no = models.CharField(max_length=100, unique=True)
    model = models.CharField(
        max_length=30,
        choices=MODEL_TYPE.choices,
    )
    weight_limit = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(500)],
    )
    battery = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)],
    )
    state = models.CharField(
        choices=DRONE_STATUS.choices,
        max_length=15,
        default=DRONE_STATUS.IDLE,
    )

    class Meta:
        verbose_name = 'Drone'
        verbose_name_plural = 'Drones'

    def __str__(self):
        return f'{self.model} - {self.serial_no} '

    def add_battery_log(self):
        pass


class Medication(GenericModel):
    name = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField()
    code = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medication/')

    class Meta:
        verbose_name = 'Medication'
        verbose_name_plural = 'Medications'

    def __str__(self):
        return self.name


class MedicationCharged(GenericModel):
    drone = models.ForeignKey(
        Drone,
        related_name='medication_charged',
        on_delete=models.CASCADE,
    )
    medications = models.ManyToManyField(
        Medication,
        related_name='medication_charged',
    )
    delivered = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Medication Charged'
        verbose_name_plural = 'Medications Charged'

    def __str__(self):
        return f'{self.drone} - {self.created_at}'


class DroneLog(GenericModel):
    drone = models.OneToOneField(
        Drone,
        on_delete=models.CASCADE,
        related_name='drone_log',
    )
    battery_history = models.JSONField(
        default=list,
        blank=True,
        encoder=DjangoJSONEncoder,
    )

    class Meta:
        verbose_name = 'Drone Log'
        verbose_name_plural = 'Drone Logs'

    def __str__(self):
        return f'{self.drone}'

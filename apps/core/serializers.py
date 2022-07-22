import re
import string
from rest_framework import serializers
from apps.core.models import DRONE_STATUS, Drone, Medication, LoadedMedication


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['uuid', 'serial_no', 'model', 'weight_limit',
                  'battery', 'state', 'created_at', 'updated_at']


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['uuid', 'name', 'weight', 'code',
                  'image', 'created_at', 'updated_at']

    def validate_name(self, name):
        allowed = string.ascii_letters+string.digits+'_'+'-'

        if not re.match(r'^[%s]+$' % allowed, name):
            raise serializers.ValidationError(
                'Name must be alphanumeric, contain only letters, digits, underscore and hyphen.')

        return name

    def validate_code(self, code):
        allowed = string.ascii_uppercase + string.digits + '_'

        if not re.match(r'^[%s]+$' % allowed, code):
            raise serializers.ValidationError(
                'Code must be contain only upper case letters, underscore and numbers.'
            )

        return code


class DroneLoadingSerializer(serializers.Serializer):
    drone = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Drone.objects.all(),
    )
    drone_name = serializers.StringRelatedField(source='drone')
    medications = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Medication.objects.all(),
        many=True,
    )
    medications_data = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    delivered = serializers.BooleanField(read_only=True)

    def get_medications_data(self, obj):
        return obj.medications.values('uuid', 'name', 'weight', 'code')

    def validate_drone(self, drone):
        if drone.state != DRONE_STATUS.IDLE:
            raise serializers.ValidationError(
                'Drone must be in IDLE state.'
            )

        if drone.battery < 25:
            raise serializers.ValidationError(
                'Drone battery level must be up or equal to 25%.'
            )

        if drone.medication_loaded.filter(delivered=False).exists():
            raise serializers.ValidationError(
                'Drone must be empty. Drone currently has undelivered medications.'
            )

        return drone

    def validate(self, attrs):
        weight = 0
        for medication in attrs['medications']:
            weight += medication.weight

        if weight > attrs['drone'].weight_limit:
            raise serializers.ValidationError(
                'Drone weight limit exceeded. Drone weight limit is %s g.' % attrs[
                    'drone'].weight_limit
            )

        return attrs

    def save(self, **kwargs):
        drone = self.validated_data['drone']
        medications = self.validated_data['medications']

        drone.state = DRONE_STATUS.LOADING
        drone.save()

        load = LoadedMedication.objects.create(
            drone=drone,
        )
        load.medications.set(medications)

        self.instance = load

        return self.instance

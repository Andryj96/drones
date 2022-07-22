import re
import string
from rest_framework import serializers
from apps.core.models import Drone, Medication


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

    def validate_code(self, name):
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

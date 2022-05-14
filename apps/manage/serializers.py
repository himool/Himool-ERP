from extensions.common.base import *
from extensions.exceptions import *
from apps.manage.models import *
from apps.system.models import *
from rest_framework.serializers import ModelSerializer


class TeamSerializer(ModelSerializer):

    class Meta:
        model = Team
        read_only_fields = ['id', 'create_time']
        fields = ['number', 'expiry_time', 'user_quantity', *read_only_fields]

    def validate_number(self, value):
        if Team.objects.filter(number=value).exists():
            raise ValidationError(f'公司编号[{value}]已存在')
        return value


class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        read_only_fields = ['id']
        fields = ['number', 'name', 'model', 'serial_number', 'account_ownership', *read_only_fields]

    def validate_number(self, value):
        self.validate_unique({'number': value}, message=f'编号[{value}]已存在')
        return value


__all__ = [
    'TeamSerializer', 'DeviceSerializer',
]

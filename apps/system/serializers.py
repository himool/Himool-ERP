from django.contrib.auth.hashers import make_password
from extensions.serializers import *
from extensions.exceptions import *
from apps.system.models import *


class PermissionGroupSerializer(BaseSerializer):

    class PermissionSerializer(BaseSerializer):

        class Meta:
            model = Permission
            fields = ['id', 'name', 'code']

    permission_items = PermissionSerializer(source='permissions', many=True, label='权限')

    class Meta:
        model = PermissionGroup
        fields = ['id', 'name', 'permission_items']


class RoleSerializer(BaseSerializer):

    class Meta:
        model = Role
        read_only_fields = ['id']
        fields = ['name', 'remark', 'permissions', *read_only_fields]


class UserSerializer(BaseSerializer):

    class UserRoleSerializer(BaseSerializer):

        class Meta:
            model = Role
            fields = ['id', 'name']

    sex_display = CharField(source='get_sex_display', read_only=True, label='性别')
    role_items = UserRoleSerializer(source='roles', many=True, read_only=True, label='角色Item')

    class Meta:
        model = User
        read_only_fields = ['id', 'sex_display', 'is_manager', 'role_items', 'permissions', 'create_time']
        fields = ['username', 'name', 'phone', 'email', 'sex', 'roles', 'is_active', *read_only_fields]

    def validate_username(self, value):
        self.validate_unique({'username': value}, message=f'用户名[{value}]已存在')
        return value

    def validate_roles(self, instances):
        instances = self.validate_foreign_key_set(Role, instances, message='角色不存在')
        return instances

    def create(self, validated_data):
        validated_data['password'] = make_password(self.team.number)
        return super().create(validated_data)

    def save(self, **kwargs):
        permissions = []
        if roles := self.validated_data.get('roles'):
            permissions = {permission.code for role in roles.prefetch_related('permissions').all()
                           for permission in role.permissions.all()}

        kwargs['permissions'] = list(permissions)
        return super().save(**kwargs)


__all__ = [
    'PermissionGroupSerializer',
    'RoleSerializer', 'UserSerializer',
]

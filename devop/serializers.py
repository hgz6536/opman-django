# -*-coding:UTF-8 -*-
from rest_framework import serializers
from opman.models import *
from opman.models import MyUser as User
from opman.models import RoleList, PermissonList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'last_login',
                  'is_superuser',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_staff',
                  'is_active',
                  'date_joined')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleList
        fields = ('id', 'name')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissonList
        fields = ('id', 'name', 'url')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Assets
        fields = ('id', 'service_name')


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone_Assets
        fields = ('id', 'zone_name')


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line_Assets
        fields = ('id', 'line_name')


class RaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid_Assets
        fields = ('id', 'raid_name')


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = ('id', 'assets_type', 'name', 'sn', 'buy_time', 'expire_date',
                  'buy_user', 'management_ip', 'manufacturer', 'provider',
                  'model', 'status', 'put_zone', 'group', 'business')


class ServerSerializer(serializers.ModelSerializer):
    assets = AssetsSerializer(required=False)

    #     keyfile = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = Server_Assets
        fields = ('id', 'ip', 'hostname', 'username', 'port', 'passwd',
                  'line', 'cpu', 'cpu_number', 'vcpu_number', 'keyfile',
                  'cpu_core', 'disk_total', 'ram_total', 'kernel',
                  'selinux', 'swap', 'raid', 'system', 'assets')

    def create(self, data):
        if (data.get('assets')):
            assets_data = data.pop('assets')
            assets = Assets.objects.create(**assets_data)
        else:
            assets = Assets()
        data['assets'] = assets
        server = Server_Assets.objects.create(**data)
        return server


class NetworkSerializer(serializers.ModelSerializer):
    assets = AssetsSerializer(required=False)

    class Meta:
        model = Network_Assets
        fields = ('id', 'ip', 'bandwidth', 'port_number', 'firmware',
                  'cpu', 'stone', 'configure_detail', 'assets')

    def create(self, data):
        if (data.get('assets')):
            assets_data = data.pop('assets')
            assets = Assets.objects.create(**assets_data)
        else:
            assets = Assets()
        data['assets'] = assets
        server = Network_Assets.objects.create(**data)
        return server


class DeployOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOrder
        fields = ('id', 'order_project', 'order_subject', 'order_content',
                  'order_branch', 'order_comid', 'order_tag', 'order_audit',
                  'order_status', 'order_level', 'order_cancel', 'create_time',
                  'order_user')


class ProjectConfigSerializer(serializers.ModelSerializer):
    project_number = serializers.StringRelatedField(many=True)  # ProjectNumberSerializer(required=False)

    class Meta:
        model = Project_Config
        fields = ('id', 'project_env', 'project_name', 'project_local_command',
                  'project_repo_dir', 'project_dir', 'project_exclude',
                  'project_address', 'project_repertory', 'project_status',
                  'project_remote_command', 'project_number')

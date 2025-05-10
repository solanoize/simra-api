from rest_framework import serializers

from catalogs.models import Group, GroupItem


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['owner']


class GroupItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        attr = super().to_representation(instance)

        attr['group'] = GroupSerializer(instance.group).data

        return attr

    class Meta:
        model = GroupItem
        fields = '__all__'
        read_only_fields = ['owner']
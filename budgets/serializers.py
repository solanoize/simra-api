from rest_framework import serializers

from budgets.models import Plan, PlanItem, PlanItemTemp
from catalogs.serializers import GroupItemSerializer


class PlanSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        attr = super().to_representation(instance)

        attr['total_amount'] = instance.total_amount
        attr['total_requirement'] = instance.total_requirement
        attr['total_usage'] = instance.total_usage
        attr['total_balance'] = instance.total_balance

        return attr

    class Meta:
        model = Plan
        fields = '__all__'
        read_only_fields = ['owner']


class PlanItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        attr = super().to_representation(instance)

        attr['plan'] = PlanSerializer(instance.plan).data
        attr['group_item'] = GroupItemSerializer(instance.group_item).data
        attr['balance'] = instance.balance

        return attr

    class Meta:
        model = PlanItem
        fields = '__all__'
        read_only_fields = ['owner', 'plan',
                            'group_item', 'amount',
                            'requirement', 'balance']


class PlanItemTempSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        amount = attrs.get('amount', 0)
        requirement = attrs.get('requirement', 0)
        errors = {}

        if amount <= 0:
            errors['amount'] = 'Amount must be greater than 0'

        if requirement <= 0:
            errors['requirement'] = 'Requirement must be greater than 0'

        if requirement > amount:
            errors['requirement'] = 'Requirement must be less than or equal to the available amount'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def to_representation(self, instance):
        attr = super().to_representation(instance)
        attr['group_item'] = GroupItemSerializer(instance.group_item).data

        return attr

    class Meta:
        model = PlanItemTemp
        fields = '__all__'
        read_only_fields = ['owner', 'group_item']
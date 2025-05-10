from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from catalogs.models import GroupItem


def validate_positive(value):
    if value <= 0:
        raise ValidationError('Value must be greater than zero.')


class Plan(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    @property
    def total_amount(self):
        return self.planitem_set.aggregate(total=Sum('amount'))['total'] or 0

    @property
    def total_requirement(self):
        return self.planitem_set.aggregate(total=Sum('requirement'))['total'] or 0

    @property
    def total_usage(self):
        return self.planitem_set.aggregate(total=Sum('usage'))['total'] or 0

    @property
    def total_balance(self):
        return self.total_amount - self.total_usage

    def __str__(self):
        return self.title


class PlanItem(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    group_item = models.ForeignKey(GroupItem, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    requirement = models.PositiveIntegerField()
    usage = models.PositiveIntegerField()

    @property
    def balance(self):
        return self.amount - self.usage

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan.name

    class Meta:
        unique_together = ('plan', 'group_item', 'owner')


class PlanItemTemp(models.Model):
    group_item = models.ForeignKey(GroupItem, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    requirement = models.PositiveIntegerField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group_item', 'owner')


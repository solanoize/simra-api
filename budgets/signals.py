from django.db.models.signals import post_save
from django.dispatch import receiver

from budgets.models import Plan, PlanItemTemp, PlanItem


@receiver(post_save, sender=Plan)
def create_plan_item(sender, instance, created, **kwargs):
    if created:
        plan_item_temps = PlanItemTemp.objects.filter(owner=instance.owner)

        plan_item_object = []

        for plan_item_temp in plan_item_temps:
            object = PlanItem(plan=instance,
                              group_item=plan_item_temp.group_item,
                              amount=plan_item_temp.amount,
                              requirement=plan_item_temp.requirement,
                              usage=0,
                              owner=instance.owner)
            plan_item_object.append(object)

        PlanItem.objects.bulk_create(plan_item_object)

        # Delete plan item temps
        plan_item_temps.delete()

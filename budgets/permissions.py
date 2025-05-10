from rest_framework import permissions


class PlanShouldHavePlanItemTemp(permissions.BasePermission):
    message = "Plan should have items to create and amount/requirement must be greater than 0"

    def has_permission(self, request, view):
        if request.method == 'POST':
            plan_item_temps = request.user.planitemtemp_set.all()

            if not plan_item_temps.exists():
                return False

            # Periksa apakah ada PlanItemTemp dengan requirement atau amount <= 0
            for item in plan_item_temps:
                if item.requirement <= 0 or item.amount <= 0:
                    return False

        return True

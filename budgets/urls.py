from django.urls import path

from budgets.views import PlanListView, PlanDetailView, PlanItemListView, PlanItemDetailView, PlanItemTempListView, \
    PlanItemTempDetailView, plan_item_temp_init

app_name = 'budgets'

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plan-list-view'),
    path('plans/<int:pk>/', PlanDetailView.as_view(), name='plan-detail-view'),
    path('plan-items/', PlanItemListView.as_view(), name='plan-item-list-view'),
    path('plan-items/<int:pk>/', PlanItemDetailView.as_view(), name='plan-item-detail-view'),
    path('plan-item-temps/', PlanItemTempListView.as_view(), name='plan-item-temp-list-view'),
    path('plan-item-temps/<int:pk>/', PlanItemTempDetailView.as_view(), name='plan-item-temp-detail-view'),
    path('plan-item-temps/initialize/', plan_item_temp_init, name='plan-item-temp-init'),
]
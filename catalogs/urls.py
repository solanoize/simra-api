from django.urls import path

from catalogs.views import GroupListView, GroupDetailView, GroupItemListView, GroupItemDetailView

app_name = 'catalogs'

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group-list-view'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail-list-view'),
    path('group-items/', GroupItemListView.as_view(), name='group-item-list-view'),
    path('group-items/<int:pk>/', GroupItemDetailView.as_view(), name='budget-item-detail-view'),
]
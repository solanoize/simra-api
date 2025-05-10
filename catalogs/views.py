from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwnerOnly
from catalogs.models import Group, GroupItem
from catalogs.serializers import GroupSerializer, GroupItemSerializer


class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ['^title', '^origin']
    filterset_fields = ['title', 'origin']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class GroupItemListView(generics.ListCreateAPIView):
    queryset = GroupItem.objects.all()
    serializer_class = GroupItemSerializer
    search_fields = ['name']
    filterset_fields = ['name', 'group']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupItem.objects.all()
    serializer_class = GroupItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
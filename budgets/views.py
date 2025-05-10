from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsOwnerOnly
from budgets.models import Plan, PlanItem, PlanItemTemp
from budgets.permissions import PlanShouldHavePlanItemTemp
from budgets.serializers import PlanSerializer, PlanItemSerializer, PlanItemTempSerializer
from catalogs.models import GroupItem


class PlanListView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    search_fields = ['^title', ]
    filterset_fields = ['title',]
    permission_classes = [IsAuthenticated, PlanShouldHavePlanItemTemp]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlanDetailView(generics.RetrieveAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class PlanItemListView(generics.ListAPIView):
    queryset = PlanItem.objects.all()
    serializer_class = PlanItemSerializer
    search_fields = ['^plan__title', '^group_item__name']
    filterset_fields = ['plan', 'group_item',
                        'amount', 'requirement',
                        'usage']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlanItemDetailView(generics.RetrieveUpdateAPIView):
    queryset = PlanItem.objects.all()
    serializer_class = PlanItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class PlanItemTempListView(generics.ListAPIView):
    queryset = PlanItemTemp.objects.all()
    serializer_class = PlanItemTempSerializer
    search_fields = ['^group_item__name']
    filterset_fields = ['group_item',
                        'amount', 'requirement']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class PlanItemTempDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanItemTemp.objects.all()
    serializer_class = PlanItemTempSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


@api_view(['POST'])
def plan_item_temp_init(request):
    # Remove terlebih dahulu semua plan item temp sebelumnya
    PlanItemTemp.objects.filter(owner=request.user).delete()

    # Ambil semua group item
    group_items = GroupItem.objects.filter(owner=request.user)

    bulks = []
    for group_item in group_items:
        bulks.append(
            PlanItemTemp(group_item=group_item, amount=0,
                         requirement=0, owner=request.user)
        )

    PlanItemTemp.objects.bulk_create(bulks)
    return Response({"ok": True}, status=status.HTTP_201_CREATED)




from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from purchase.serializers import GroupSerializer, UserSerializer
from purchase.serializers import SupplierSerializer, OrderSerializer, LineItemSerializer
from purchase.models import Supplier, Order, LineItem
from drf_spectacular.utils import extend_schema, extend_schema_view
from purchase.filters import OrderFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that supplier to be viewed or edited.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that order to be viewed or edited.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    filterset_class = OrderFilter


class LineItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that line item to be viewed or edited.
    """
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
    permission_classes = [permissions.IsAuthenticated]

from django.contrib.auth.models import Group, User
from rest_framework import serializers
from purchase.models import Supplier, Order, LineItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class LineItemSerializer(serializers.ModelSerializer):
    # computed field
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    line_items = LineItemSerializer(many=True)
    order_number = serializers.PrimaryKeyRelatedField(read_only=True)

    # computed field
    total_quantity = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    total_tax = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_quantity', 'total_amount', 'total_tax']

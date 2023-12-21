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


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order


class LineItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LineItem

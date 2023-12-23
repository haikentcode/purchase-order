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

    def to_internal_value(self, data):
        if self.instance is None:  # Check if creating a new instance
            return {**super().to_internal_value(data), 'id': data.get('id')}
        else:  # Updating existing instance, don't include 'id' in internal representation
            return super().to_internal_value(data)


class LineItemSerializer(serializers.ModelSerializer):
    # computed field
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = '__all__'
        extra_kwargs = {
            'purchase_order': {'required': False},
        }


class OrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer()
    line_items = LineItemSerializer(many=True)
    order_number = serializers.PrimaryKeyRelatedField(read_only=True)

    # computed field
    total_quantity = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    total_tax = serializers.ReadOnlyField()

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier')
        supplier_id = supplier_data.get('id')

        # Check if a supplier with the given ID already exists
        try:
            supplier = Supplier.objects.get(id=supplier_id)

            # Update the existing supplier with the new data
            for key, value in supplier_data.items():
                setattr(supplier, key, value)

            supplier.save()
        except Supplier.DoesNotExist:
            # Create a new supplier if it doesn't exist
            supplier = Supplier.objects.create(**supplier_data)

        line_items_data = validated_data.pop('line_items')

        order = Order.objects.create(supplier=supplier, **validated_data)

        for line_item_data in line_items_data:
            LineItem.objects.create(purchase_order=order, **line_item_data)

        return order

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_quantity', 'total_amount', 'total_tax']

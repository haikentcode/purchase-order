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
    
    def create(self, validated_data):
        instance_id = validated_data.get('id')
        
        if instance_id:
            # If an ID is provided, try to update the instance
            instance, created = Supplier.objects.update_or_create(id=instance_id, defaults=validated_data)
            return instance

        # If no ID is provided, create a new instance
        return Supplier.objects.create(**validated_data)


class LineItemSerializer(serializers.ModelSerializer):
    # computed field
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = '__all__'
        extra_kwargs = {
            'purchase_order': {'required': False},
        }

    def to_internal_value(self, data):
        if self.instance is None:  # Check if creating a new instance
            return {**super().to_internal_value(data), 'id': data.get('id')}
        else:  # Updating existing instance, don't include 'id' in internal representation
            return super().to_internal_value(data)


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
        supplier_serializer = SupplierSerializer(data=supplier_data)
        supplier_serializer.is_valid(raise_exception=True)
        supplier_serializer.save()


        line_items_data = validated_data.pop('line_items')

        order = Order.objects.create(supplier=supplier_serializer.instance, **validated_data)

        line_item_serializer = LineItemSerializer(data=line_items_data, many=True)
        line_item_serializer.is_valid(raise_exception=True)
        line_item_serializer.save(purchase_order=order)


        return order

    def update(self, instance, validated_data):

        supplier_data = validated_data.pop('supplier')
        supplier_serializer = SupplierSerializer(data=supplier_data)
        supplier_serializer.is_valid(raise_exception=True)
        supplier_serializer.save()

        instance.supplier = supplier_serializer.instance

        line_items_data = validated_data.pop('line_items')

        # Update the line items
        updated_line_item_ids = set()
        for line_item_data in line_items_data:
            line_item_id = line_item_data.get('id')
            if line_item_id:
                # If line item ID is provided, update the existing line item
                line_item = LineItem.objects.get(id=line_item_id)
                for field_name, field_value in line_item_data.items():
                    setattr(line_item, field_name, field_value)
                line_item.save()
                updated_line_item_ids.add(line_item_id)
            else:
                # If no line item ID is provided, create a new line item
                new_line_item = LineItem.objects.create(
                    purchase_order=instance, **line_item_data)

                updated_line_item_ids.add(new_line_item.id)

        # Delete line items that are not present in the updated data
        instance.line_items.exclude(id__in=updated_line_item_ids).delete()

        # Update other fields of the order if needed
        instance.save()

        return instance

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_quantity',
                            'total_amount', 'total_tax']

from django.core.management.base import BaseCommand
from purchase.models import Supplier, Order, LineItem, OrderNumber


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Sample supplier data
        suppliers_data = [
            {"name": "Supplier 1", "email": "supplier1@email.com"},
            {"name": "Supplier 2", "email": "supplier2@email.com"},
            {"name": "Supplier 3", "email": "supplier3@email.com"},
            # Add more suppliers as needed
        ]

        # Create Supplier instances
        for supplier_data in suppliers_data:
            supplier = Supplier.objects.create(**supplier_data)

            order_data = {
                "supplier": supplier,
            }

            # Create Order instance
            order = Order.objects.create(**order_data)

            # Sample line item data
            line_item_data = {
                "item_name": "Item 1",
                "quantity": 5,
                "price_without_tax": 20.0,
                "tax_name": 1,
                "tax_amount": 2.0,
                "purchase_order": order,
            }

            # Create LineItem instance
            line_item = LineItem.objects.create(**line_item_data)

        self.stdout.write(self.style.SUCCESS('Successfully added sample data'))

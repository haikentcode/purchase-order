from django.core.management.base import BaseCommand
from purchase.models import Supplier, Order, LineItem


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

            # Sample order data
            order_data = {
                "supplier": supplier,
                "order_time": "2023-01-01T12:00:00",  # Replace with actual date and time
                "order_number": 1,  # Replace with a unique order number
                "total_quantity": 10,
                "total_amount": 100.0,
                "total_tax": 10.0,
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
                "line_total": 110.0,
                "purchase_order": order,
            }

            # Create LineItem instance
            line_item = LineItem.objects.create(**line_item_data)

        self.stdout.write(self.style.SUCCESS('Successfully added sample data'))

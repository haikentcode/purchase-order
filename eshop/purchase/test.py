# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from purchase.models import Supplier, OrderNumber, Order, LineItem
from django.contrib.auth.models import User
import json
from rest_framework.test import APITestCase
from django.urls import reverse


class ConsoleColors:
    """
    ANSI escape codes for text color in the console
    """
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


DEBUG_PRINT = True


def pprint(response):

    if DEBUG_PRINT:
        try:
            content = json.loads(response.content.decode('utf-8'))
            pretty_content = json.dumps(content, indent=2)
            # print(f"{ConsoleColors.YELLOW}Response Content:\n{pretty_content}{ConsoleColors.RESET}")

        except json.JSONDecodeError:
            print(
                f"{ConsoleColors.RED}Unable to decode response content as JSON:\n{content}{ConsoleColors.RESET}")


class SupplierAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.client = APIClient()
        self.supplier_data = {
            'name': 'Test Supplier',
            'email': 'test@example.com',
        }
        self.supplier = Supplier.objects.create(**self.supplier_data)

    def test_create_supplier(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            reverse('supplier-list'), self.supplier_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 2)

    def test_update_supplier(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        updated_data = {
            'name': 'Updated Supplier',
            'email': 'updated@example.com',
        }
        response = self.client.put(
            reverse('supplier-detail', args=[self.supplier.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, updated_data['name'])
        self.assertEqual(self.supplier.email, updated_data['email'])

    def test_delete_supplier(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        response = self.client.delete(
            reverse('supplier-detail', args=[self.supplier.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)


class LineItemViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a sample supplier
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.supplier_data = {'name': 'Supplier 1',
                              'email': 'supplier1@example.com'}
        self.supplier = Supplier.objects.create(**self.supplier_data)

        # Create a sample order
        self.order_data = {'supplier': self.supplier,
                           'order_time': '2023-01-01T12:00:00Z'}
        self.order = Order.objects.create(**self.order_data)

        # Create a sample line item
        self.line_item_data = {
            'item_name': 'Test Item',
            'quantity': 2,
            'price_without_tax': 15.0,
            'tax_name': 'GST 5%',
            'tax_amount': 1.0,
            'purchase_order': self.order
        }
        self.line_item = LineItem.objects.create(**self.line_item_data)

        # Set up the URL for the LineItemViewSet
        # Adjust the URL name based on your project
        self.url = reverse('lineitem-list')

    def test_create_line_item(self):

        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        data = {
            'item_name': 'New Item',
            'quantity': 3,
            'price_without_tax': 20.0,
            'tax_name': 'VAT 10%',
            'tax_amount': 2.0,
            'purchase_order': self.order.id
        }

        # Send a POST request to create a new line item
        response = self.client.post(self.url, data, format='json')

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the line item was actually created in the database
        created_line_item = LineItem.objects.get(id=response.data['id'])
        self.assertEqual(created_line_item.item_name, 'New Item')

    def test_get_line_item(self):

        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        # Send a GET request to retrieve the existing line item
        response = self.client.get(
            reverse('lineitem-detail', args=[self.line_item.id]))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Optionally, check that the response data contains the expected fields
        self.assertIn('id', response.data)
        self.assertIn('item_name', response.data)
        self.assertIn('quantity', response.data)
        # Add more assertions based on your data model

    def test_update_line_item(self):

        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        data = {
            'item_name': 'Updated Item',
            'quantity': 4,
            'price_without_tax': 25.0,
            'tax_name': 'VAT 15%',
            'tax_amount': 3.0,
            'purchase_order': self.order.id
        }

        # Send a PUT request to update the existing line item
        response = self.client.put(
            reverse('lineitem-detail', args=[self.line_item.id]), data, format='json')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the line item was actually updated in the database
        updated_line_item = LineItem.objects.get(id=self.line_item.id)
        self.assertEqual(updated_line_item.item_name, 'Updated Item')

    def test_delete_line_item(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        # Send a DELETE request to delete the existing line item
        response = self.client.delete(
            reverse('lineitem-detail', args=[self.line_item.id]))

        # Check that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the line item was actually deleted from the database
        with self.assertRaises(LineItem.DoesNotExist):
            LineItem.objects.get(id=self.line_item.id)


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.client = APIClient()

        # Create a test supplier
        self.supplier = Supplier.objects.create(
            name='Test Supplier', email='test@example.com')

        # Create a test order with line items
        self.order = Order.objects.create(supplier=self.supplier)
        LineItem.objects.create(
            item_name='Test Item 1', quantity=2, price_without_tax=5.0, tax_name='GST', tax_amount=1.0, purchase_order=self.order)
        LineItem.objects.create(
            item_name='Test Item 2', quantity=3, price_without_tax=8.0, tax_name='VAT', tax_amount=1.5, purchase_order=self.order)

    def test_create_order(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        data = {
            "supplier": {
                "name": "my supplier",
                "email": "email@email.com",
            },
            "line_items": [
                {
                    "item_name": "test prod",
                    "quantity": 1,
                    "price_without_tax": 10.00,
                    "tax_name": "GST 5%",
                    "tax_amount": 0.50
                },
                {
                    "item_name": "test prod",
                    "quantity": 3,
                    "price_without_tax": 10.00,
                    "tax_name": "GST 5%",
                    "tax_amount": 0.50
                }
            ]
        }

        response = self.client.post(reverse('order-list'), data, format='json')
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_without_line_items(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        data = {
            "supplier": {
                "name": "my supplier",
                "email": "email@email.com"
            },
        }

        response = self.client.post(reverse('order-list'), data, format='json')
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_supplier(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        data = {
            "line_items": [
                {
                    "item_name": "test prod",
                    "quantity": 1,
                    "price_without_tax": "10.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.50"
                }
            ]
        }

        response = self.client.post(reverse('order-list'), data, format='json')
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_pre_exist_supplier(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        supplier = Supplier.objects.create(
            name='Test Supplier', email='test@example.com')

        updated_supplier_data = {
            "id": supplier.id,
            "name": "supplier_updated_name",
            "email": "supplier_updated_email@email.com"
        }

        data = {
            "supplier": updated_supplier_data,
            "line_items": [
                {
                    "item_name": "test prod",
                    "quantity": 1,
                    "price_without_tax": "10.00",
                    "tax_name": "GST 5%",
                    "tax_amount": "0.50"
                }
            ]
        }

        response = self.client.post(reverse('order-list'), data, format='json')
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        content = response.data
        self.assertEqual(
            updated_supplier_data["id"], content["supplier"]["id"])
        self.assertEqual(
            updated_supplier_data["name"], content["supplier"]['name'])
        self.assertEqual(
            updated_supplier_data["email"], content["supplier"]['email'])

    def test_filter_orders_by_supplier_name(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        # Test filter by supplier_name
        supplier_name = 'Test Supplier'
        response = self.client.get(
            reverse('order-list'), {'supplier_name': supplier_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        supplier_name = 'Test'
        response = self.client.get(
            reverse('order-list'), {'supplier_name': supplier_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        supplier_name = 'Testt SSupplier'
        response = self.client.get(
            reverse('order-list'), {'supplier_name': supplier_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_orders_by_item_name(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        # Test filter by item_name
        item_name = 'Test Item 1'
        response = self.client.get(
            reverse('order-list'), {'item_name': item_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test filter by item_name
        item_name = 'Test'
        response = self.client.get(
            reverse('order-list'), {'item_name': item_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test filter by item_name
        item_name = 'TRest ItMem'
        response = self.client.get(
            reverse('order-list'), {'item_name': item_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_orders_by_supplier_and_item_name(self):
        # Log in the user to establish a session
        self.client.login(username='testuser', password='testpassword')

        # Test filter by both supplier_name and item_name
        supplier_name = 'Test Supplier'
        item_name = 'Test Item 1'
        response = self.client.get(
            reverse('order-list'), {'supplier_name': supplier_name, 'item_name': item_name})
        pprint(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

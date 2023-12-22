from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Supplier(models.Model):
    name = models.CharField(max_length=1024)
    email = models.EmailField()

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def __str__(self):
        return self.name


class OrderNumber(models.Model):
    pass


class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_time = models.DateTimeField(editable=False)
    order_number = models.OneToOneField(
        OrderNumber, on_delete=models.CASCADE, editable=False)

    # Calculated Feild can be added as property
    total_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    total_amount = models.FloatField(validators=[MinValueValidator(0.0)])
    total_tax = models.FloatField(validators=[MinValueValidator(0.0)])

    def save(self, *args, **kwargs):
        # Check if the order_number is not set
        if not self.order_number:
            # Create a new OrderNumber instance
            order_number_instance = OrderNumber.objects.create()
            self.order_number = order_number_instance
            self.order_time = timezone.now()

        super().save(*args, **kwargs)

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.line_items.all())

    @property
    def total_amount(self):
        return sum(item.line_total for item in self.line_items.all())

    @property
    def total_tax(self):
        return sum(item.tax_amount for item in self.line_items.all())

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-order_time']

    def __str__(self):
        return f"Order {self.order_number} - {self.order_time}"


class LineItem(models.Model):
    item_name = models.CharField(max_length=1024)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price_without_tax = models.FloatField(validators=[MinValueValidator(0.0)])
    tax_name = models.CharField(max_length=1024)
    tax_amount = models.FloatField(validators=[MinValueValidator(0.0)])
    purchase_order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='line_items')

    @property
    def line_total(self):
        return self.tax_amount + self.price_without_tax

    class Meta:
        verbose_name = "Line Item"
        verbose_name_plural = "Line Items"
        ordering = ['item_name', 'quantity']

    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"

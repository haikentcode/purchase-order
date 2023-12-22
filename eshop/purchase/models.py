from django.db import models
from django.core.validators import MinValueValidator


class Supplier(models.Model):
    name = models.CharField(max_length=1024)
    email = models.EmailField()

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    order_number = models.IntegerField(db_index=True)
    total_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    total_amount = models.FloatField(validators=[MinValueValidator(0.0)])
    total_tax = models.FloatField(validators=[MinValueValidator(0.0)])

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
    tax_name = models.IntegerField(validators=[MinValueValidator(0)])
    tax_amount = models.FloatField(validators=[MinValueValidator(0.0)])
    line_total = models.FloatField(validators=[MinValueValidator(0.0)])
    purchase_order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='line_items')

    class Meta:
        verbose_name = "Line Item"
        verbose_name_plural = "Line Items"
        ordering = ['item_name', 'quantity']

    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"

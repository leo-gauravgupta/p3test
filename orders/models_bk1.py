from django.db import models

# Create your models here.

class Menu(models.Model):
    item = models.CharField(max_length=64)
    subItem = models.CharField(max_length=64)
    priceSmall = models.FloatField(blank=True)
    priceLarge = models.FloatField(blank=True)

    def __str__(self):
        return f"Item: {self.item}:, Sub-Item: {self.subItem}, Price-Small: {self.priceSmall}, Price.Large: {self.priceLarge}"

class Order(models.Model):
    orderItem = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="orderItems")
    orderPrice = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="orderPrices")
    orderQty = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.orderItem} {self.orderPrice} {self.orderQty}"

class Customer(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    custUserID = models.CharField(max_length=64)
    orders = models.ManyToManyField(Order, blank=True, related_name="custOrders")

    def __str__(self):
        return f"{self.first} {self.last} {self.custUserID}"

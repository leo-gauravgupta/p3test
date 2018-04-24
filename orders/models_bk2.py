from django.db import models

# Create your models here.

#class Topping(models.Model):
#    topping = models.CharField(max_length=64)

#    def __str__(self):
#        return f"Item: {self.topping}"

class Menu(models.Model):
    item = models.CharField(max_length=64)
    subItem = models.CharField(max_length=64)
#    toppings = models.ManyToManyField(Topping, blank=True)
    priceSmall = models.FloatField(blank=True)
    priceLarge = models.FloatField(blank=True)

    def __str__(self):
        return f"Item: {self.item}, Sub-Item: {self.subItem}"

class Order(Menu):
    orderSizes = (
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('Standard', 'Standard')
    )
    orderSize = models.CharField(max_length=10, choices=orderSizes)
    orderPrice = models.FloatField(blank=True)
    orderQty = models.IntegerField()
    orderCost = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.id} --> Order-Item: {self.orderItem}, Order-Size: {self.orderSize}, Order-Price: {self.orderPrice}, Order-Qty: {self.orderQty}"

class Customer(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    custUserID = models.CharField(max_length=64)
    orders = models.ManyToManyField(Order, blank=True, related_name="custOrders")

    def __str__(self):
        return f"{self.first} {self.last} {self.custUserID}"

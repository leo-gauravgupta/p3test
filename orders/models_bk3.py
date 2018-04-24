from django.db import models

# Create your models here.

class Topping(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"

class Item(models.Model):
    item = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.item}"

class Subitem(models.Model):
    subItem = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.subItem}"

class Pricesmall(models.Model):
    priceSmall = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.priceSmall}"

class Pricelarge(models.Model):
    priceLarge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.priceLarge}"

class Menu(models.Model):
    items = models.OneToOneField(Item, blank=True, on_delete=models.CASCADE)
    subItems = models.OneToOneField(Subitem, blank=True, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)
    priceSmalls = models.OneToOneField(Pricesmall, blank=True, on_delete=models.CASCADE)
    priceLarges = models.OneToOneField(Pricelarge, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Item: {self.items}, Sub-Item: {self.subItems}"

#class Menu(models.Model):
#    item = models.CharField(max_length=64)
#    subItem = models.CharField(max_length=64)
#    toppings = models.ManyToManyField(Topping, blank=True)
#    priceSmall = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#    priceLarge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

#    def __str__(self):
#        return f"Item: {self.item}, Sub-Item: {self.subItem}"

class Order(Menu):
    #menu_ptr = models.OneToOneField(Menu, parent_link=True, on_delete=models.CASCADE)
    #item_ptr = models.OneToOneField(Menu, parent_link=True, on_delete=models.CASCADE)
    #subItem_ptr = models.OneToOneField(Menu, parent_link=True, on_delete=models.CASCADE)
    #toppings_ptr = models.OneToOneField(Menu, parent_link=True, on_delete=models.CASCADE)
    #priceSmall_ptr = models.OneToOneField(Menu, parent_link=True, on_delete=models.CASCADE)
    #priceLarge_ptr = models.OneToOneField(Menu, parent_link=True, on_delete=models.CASCADE)
    orderSizes = (
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('Standard', 'Standard')
    )
    orderSize = models.CharField(max_length=10, choices=orderSizes)
    orderPrice = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    orderQty = models.IntegerField()
    orderCost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.id} --> Order-Item: {self.orderItem}, Order-Size: {self.orderSize}, Order-Price: {self.orderPrice}, Order-Qty: {self.orderQty}"

class Customer(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    custUserID = models.CharField(max_length=64)
    orders = models.ManyToManyField(Order, blank=True, related_name="custOrders")

    def __str__(self):
        return f"{self.first} {self.last} {self.custUserID}"

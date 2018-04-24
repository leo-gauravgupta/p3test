from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Topping, Menu, Order, Customer

# Create your views here.
def index(request):
    context = {
        "menus": Menu.objects.all()
    }
    #return HttpResponse("Flights")
    return render(request, "menus/index.html", context)

def order(request):
    context = {
        "orders": Menu.objects.all(),
        "toppings": Topping.objects.all(),
        "sizes": Order.objects.all(),
        "customers": Customer.objects.all()
    }

    return render(request, "menus/order.html", context)

#def order_subitems(request):
#    item = request.GET.get('item')
#    subItem = Menu.objects.filter(item=item).order_by('subItem')
#    return render(request, "menus/order.html", {'subItem': subItem})


def orderplace(request):
#    try:
    customer_id = int(request.POST["Customer"])
    order_item = request.POST["Item"]
    order_subItem = str(request.POST["Subitem"])
    order_toppings = str(request.POST["Toppings"])
    orderSize = str(request.POST["Size"])
    orderPrice = float(0)
    orderQty = int(request.POST["Quantity"])
    orderCost = float(0)
    customer = Customer.objects.get(pk=customer_id)

    #Check prices:
    order_var1 = Menu.objects.get(item__contains=order_item, subItem=order_subItem)
    order_price_small = order_var1.priceSmall
    order_price_large = order_var1.priceLarge

    priceCheck = "Small"

    if (orderSize == "Small"):
        priceCheck = order_price_small
    elif (orderSize == "Large"):
        priceCheck = order_price_large

    orderPrice = priceCheck
    order_cost = orderPrice * orderQty


    #except KeyError:
        #return render(request, "menus/error.html", {"message": "No selection."})
    #except Menu.DoesNotExist:
    #    return render(request, "menus/error.html", {"message": "No flight."})
    #except Passenger.DoesNotExist:
    #    return render(request, "menus/error.html", {"message": "No passenger."})

    #order = Order(order_item=order_item, order_subItem=order_subItem, order_toppings=order_toppings, orderSize=orderSize, orderPrice=orderPrice, orderQty=orderQty, orderCost=orderCost)
    order = Order(order_item=order_item, order_subItem=order_subItem, order_toppings=order_toppings, orderSize=orderSize, orderPrice=orderPrice, orderQty=orderQty, orderCost=order_cost)
    order.save()
    order_create_id = Order.objects.latest('id').id
    customer.orders.add(order_create_id)
    #order.save()
    #customer.orders.add(order)
    #return HttpResponseRedirect(reverse("order"))
    return render(request, "menus/checkout.html", context)
    #return HttpResponseRedirect(reverse("index"))

    #return HttpResponseRedirect(reverse("checkout", args=(order_create_id,)))

    #def checkout(request):
    #    context = {
    #        "orders": Menu.objects.all(),
    #        "toppings": Topping.objects.all(),
    #        "sizes": Order.objects.all(),
    #        "customers": Customer.objects.all()
    #    }
#
#    return render(request, "menus/checkout.html", context)

from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django import forms
from .forms import UserRegistrationForm

from .models import Topping, Menu, Order, Customer

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "menus/login.html", {"message": None})
    context = {
        "menus": Menu.objects.all(),
        "user": request.user
    }

    first = request.user.first_name
    last = request.user.last_name
    custUserID = request.user.username

    try:
        login_check = Customer.objects.get(custUserID=custUserID)
    except Customer.DoesNotExist:
        cust = Customer(first=first, last=last, custUserID=custUserID)
        cust.save()

    login_check = Customer.objects.get(custUserID=custUserID)
    if login_check is None:
        cust = Customer(first=first, last=last, custUserID=custUserID)
        cust.save()

    return render(request, "menus/menuindex.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "menus/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "menus/login.html", {"message": "Logged out."})

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            first_name = userObj['first_name']
            last_name = userObj['last_name']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists()):
                new_user = User.objects.create_user(username, email, password)
                new_user.is_active = True
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError("Username already exists.")
    else:
        form = UserRegistrationForm()
    return render(request, 'menus/register.html', {'form': form})


def menuindex(request):
    context = {
        "menus": Menu.objects.all(),
        "user": request.user
    }
    #return HttpResponse("Flights")
    return render(request, "menus/menuindex.html", context)

def order(request):
    login_user = request.user.username
    login_customer = Customer.objects.get(custUserID=login_user)
    context = {
        "user": request.user,
        "orders": Menu.objects.all(),
        "toppings": Topping.objects.all(),
        "sizes": Order.objects.all(),
        "customers": login_customer
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

    orders_disp = Order.objects.get(id=order_create_id)
    context = {
        "orders": orders_disp,
        "customer": customer
    }
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

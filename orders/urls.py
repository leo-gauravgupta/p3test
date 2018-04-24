from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order/", views.order, name="order"),
    path("orderplace/", views.orderplace, name="orderplace")
    #path("checkout/", views.checkout, name="checkout")
]

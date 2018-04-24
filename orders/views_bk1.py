from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Menu

# Create your views here.
def index(request):
    context = {
        "menus": Menu.objects.all()
    }
    #return HttpResponse("Flights")
    return render(request, "menus/index.html", context)

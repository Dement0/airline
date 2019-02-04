from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger

import stripe

# Create your views here.
def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        # pk = primary key
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        # Pass also non passengers info to be able to list them as passengers to be added
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):
    try:
        # try to extract the "passenger" info from the request
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        raise Http404("No selection.")
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")
    except Passenger.DoesNotExist:
        raise Http404("Passenger does not exist.")

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))


def checkout(request):
    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form
    token = request.POST.get('stripeToken')

    # charge using the token
    charge = stripe.Charge.create(
        amount=2999,
        currency='usd',
        description='Example charge',
        source=token,
    )
    print(charge)

    # retrieve single charge
    retrieved = stripe.Charge.retrieve(
        charge["id"],
        api_key="sk_test_4eC39HqLyjWDarjtT1zdp7dc"
    )
    print(retrieved)
    return HttpResponseRedirect(reverse("index"))

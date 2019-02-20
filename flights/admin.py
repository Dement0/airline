from django.contrib import admin

from .models import Airport, Flight, Passenger

# Register your models here.

class PassengerInline(admin.StackedInline):
    """
        Inherits from the built-in class StackedInline that allows for the
        addition of new relationships between objects.

        Represents the place in the UI where a flight’s passengers can be modified
    """
    # Passenger.flights.through refers to the in-between table linking flights and passengers
    # By setting model to this in-between table, that table is associated with PassengerInline
    model = Passenger.flights.through

    # The number of passengers which can be edited at a time
    extra = 1


class FlightAdmin(admin.ModelAdmin):
    """
    Inherits from ModelAdmin, and contains a special set of configurations
    only to be used when editing passengers.

    These settings are applied by passing FlightAdmin to admin.site.regiser
    """
    # Inlines contains all additional inline modification sections for the admin page
    inlines = [PassengerInline]


class PassengerAdmin(admin.ModelAdmin):
    """
    filter_horizontal helps to manipulate what flights a passenger is on.

    It simply allows for an additional UI element on the admin app to make it
    easy to add or remove flights that a passenger is on.
    """
    filter_horizontal = ("flights",)


admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger)

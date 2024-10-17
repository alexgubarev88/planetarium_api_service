from django.contrib import admin

from planetarium.models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    ShowSession,
    Reservation,
    Ticket
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


class ReservationAdmin(admin.ModelAdmin):
    inlines = [TicketInline]


admin.site.register(PlanetariumDome)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(ShowSession)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Ticket)

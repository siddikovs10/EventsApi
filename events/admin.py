from django.contrib import admin

from .models import (
    User,
    Event,
    Ticket,
    Booking,
    VerificationCode,
)

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(VerificationCode)

from django.contrib import admin

from .models import (
    User,
    Event,
    Ticket,
    Booking,
    VerificationCode,
    Category,
)

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Booking)
admin.site.register(VerificationCode)
admin.site.register(Category)
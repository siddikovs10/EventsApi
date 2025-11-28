from django.db import models
from .user import User
from .event import Event

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.event.title} - {self.seat_number}"

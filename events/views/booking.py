from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from events.models import Booking, Ticket
from events.serializers import BookingSerializer
from events.permissions import IsBookingOwner


class BookingListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        ticket = serializer.validated_data['ticket']
        if not ticket.is_available:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'ticket': 'Ticket is not available'})

        serializer.save(user=self.request.user)
        ticket.is_available = False
        ticket.owner = self.request.user
        ticket.save()


class BookingDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsBookingOwner]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

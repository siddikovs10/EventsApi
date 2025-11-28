from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from events.models import Ticket, Event
from events.serializers import TicketSerializer
from events.permissions import IsTicketOwner


class TicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(owner=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        event_id = request.data.get('event')

        try:
            event = Event.objects.get(pk=event_id)
            if event.organizer != request.user:
                return Response(
                    {'error': 'You can only create tickets for your own events'},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(event=event, owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTicketOwner]
    serializer_class = TicketSerializer

    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return None

    def get(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, ticket)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, ticket)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = self.get_object(pk)
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, ticket)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

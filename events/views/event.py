from rest_framework import generics, permissions
from django.db.models import Q

from ..models import Event
from ..serializers import EventSerializer
from ..permissions import IsEventOrganizer


class EventListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

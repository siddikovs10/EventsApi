from rest_framework import generics, permissions

from events.models import Event
from events.serializers import EventSerializer
from events.permissions import IsEventOrganizer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
    
    
class EventListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer
    @extend_schema(
        parameters=[
            OpenApiParameter("category", description="Filter by category id", required=False, type=int),
            OpenApiParameter("search", description="Search by title or description", required=False, type=str),
        ]
    )

    def get(self, request):
        user = request.user
        category_id = request.GET.get('category')
        search = request.GET.get('search')

        events = Event.objects.all()

        if category_id:
            events = events.filter(category_id=category_id)

        if search:
            events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

from django.urls import path
from .views import (
    RegisterView, VerifyCodeView, LoginView, UserProfileView,
    EventListCreateView, EventDetailView,
    TicketListCreateView, TicketDetailView,
    BookingListCreateView, BookingDetailView,
    ResendCodeView
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify/', VerifyCodeView.as_view(), name='verify-code'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/resend-code/', ResendCodeView.as_view(), name='resend-code'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    
    # Event
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    
    # Ticket
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    
    # Booking
    path('bookings/', BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    
    # User
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
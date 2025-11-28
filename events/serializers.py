from rest_framework import serializers
from .models import Booking, VerificationCode, Event, Ticket, User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_verified']
        read_only_fields = ['id', 'is_verified']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'user', 'ticket', 'booked_at']
        read_only_fields = ['id', 'user', 'booked_at']

class VerificationCodeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = VerificationCode
        fields = ['id', 'user', 'code', 'created_at', 'expires_at']
        read_only_fields = ['id', 'user', 'created_at', 'expires_at']


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'organizer', 'title', 'description', 'date', 'location', 'created_at']
        read_only_fields = ['id', 'organizer', 'created_at']


class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())  # ✅ Queryset qo'shildi
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'event', 'owner', 'price', 'seat_number', 'is_available']
        read_only_fields = ['id', 'owner']
        



from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import random
from events.models import User, VerificationCode
from events.serializers import UserSerializer, RegisterSerializer, LoginSerializer, VerifyCodeSerializer
from events.utils import send_verification_email

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            phone=phone,
            password=password,
            is_active=True  # foydalanuvchi aktiv
        )

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        VerificationCode.objects.create(user=user, code=code)
        send_verification_email(email, code)

        return Response(
            {'message': 'User registered. Verification code sent to email.'},
            status=status.HTTP_201_CREATED
        )

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
            verification_code = VerificationCode.objects.filter(user=user, code=code).latest('created_at')

            if verification_code.is_expired():
                return Response({'error': 'Verification code expired'}, status=400)

            user.is_verified = True
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        except VerificationCode.DoesNotExist:
            return Response({'error': 'Invalid verification code'}, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        if not user.is_verified:
            return Response({'error': 'Please verify your email first'}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ResendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        VerificationCode.objects.create(user=user, code=code)
        send_verification_email(email, code)
        return Response({"message": "New verification code sent to your email."}, status=200)

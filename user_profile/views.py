# user_profile/views.py
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from .serializers import SignedInUserSerializer


class SignedInUserView(APIView):
    """
    Retrieve the currently signed-in user's details.
    """
    permission_classes = [IsAuthenticated]  # Require the user to be authenticated

    def get(self, request):
        # Use request.user to get the signed-in user
        user = request.user
        serializer = SignedInUserSerializer(user)
        return Response(serializer.data, status=200)

class CustomRefreshToken(RefreshToken):
    def for_user(self, user):
        # Add role to the JWT token payload
        refresh = super().for_user(user)
        refresh.payload['role'] = user.role
        return refresh
    

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            # Authenticate user using phone number
            user = authenticate(request, phone_number=phone_number, password=password)

            if user is not None:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                return Response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'role': user.role,
                }, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Invalid phone number or password"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class SignInWithTokenView(APIView):
    """
    Validate an access token and return user information if the token is valid.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get("accessToken", None)

        if not token:
            return Response(
                {"error": "No access token provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Validate the token using Simple JWT
            access_token = AccessToken(token)
            user_id = access_token["user_id"]

            # Retrieve the user from the database
            user = User.objects.get(id=user_id)

            # Return user data
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": getattr(user, "role", "user"),  # Assuming 'role' is a field
                    },
                    "accessToken": str(access_token),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": "Invalid or expired access token.", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
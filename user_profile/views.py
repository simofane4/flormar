# user_profile/views.py
from rest_framework import generics, permissions, status,viewsets,serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate,get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import UserProfile,City
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny,BasePermission,IsAuthenticatedOrReadOnly
from .serializers import SignedInUserSerializer,UserProfileSerializer,CitySerializer,SellerSerializer



class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit, but allow anyone to view.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_authenticated and request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_authenticated and request.user.role == 'admin'




User = get_user_model()

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


User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Allow anyone to register

    def perform_create(self, serializer):
        # Set created_by if user is authenticated
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            serializer.save()

class UserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return UserProfile.objects.all()
        elif user.role == 'seller':
            return UserProfile.objects.filter(
                Q(role='client') & Q(assigned_seller=user)
            )
        return UserProfile.objects.filter(id=user.id)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class SellerClientsView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(
            assigned_seller=self.request.user,
            role='client'
        )





class SellerViewSet(viewsets.ModelViewSet):
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_queryset(self):
        return User.objects.filter(role='seller')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='seller')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def clients(self, request, pk=None):
        seller = self.get_object()
        clients = seller.clients.all()
        serializer = UserSerializer(clients, many=True)
        return Response(serializer.data)





class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        cities = City.objects.filter(name__icontains=query)[:10]
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)
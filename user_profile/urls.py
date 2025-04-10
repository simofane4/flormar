# user_profile/urls.py
from django.urls import path,include
from .views import (LoginView, SignInWithTokenView, SignedInUserView,UserCreateView,CityViewSet,SellerViewSet,
    UserListView,
    UserDetailView,
    SellerClientsView)
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='citie')
router.register(r'sellers', SellerViewSet, basename='seller')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
    path("sign-in-with-token/", SignInWithTokenView.as_view(), name="sign-in-with-token"),
    path('me/', SignedInUserView.as_view(), name='signed-in-user'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('seller/clients/', SellerClientsView.as_view(), name='seller-clients'),
    path('', include(router.urls)),

]

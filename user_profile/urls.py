# user_profile/urls.py
from django.urls import path
from .views import LoginView, SignInWithTokenView, SignedInUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
    path("sign-in-with-token/", SignInWithTokenView.as_view(), name="sign-in-with-token"),
    path('me/', SignedInUserView.as_view(), name='signed-in-user'),
]

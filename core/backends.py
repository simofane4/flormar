from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from user_profile.models import UserProfile

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by phone number OR username (fallback)
            user = UserProfile.objects.get(
                Q(phone_number=username) | 
                Q(username=username)
            )
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None
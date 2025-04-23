from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_profile.models import UserProfile, UserRole, City

class UserProfileForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserRole.choices)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    assigned_seller = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role=UserRole.SELLER), 
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'password1', 
            'password2',
            'role',
            'profile_image',
            'phone_number',
            'discount_percentage',
            'assigned_seller',
            'city'
        ]
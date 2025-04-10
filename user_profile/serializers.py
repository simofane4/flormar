
# Add your serializers here 
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import UserProfile ,City


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    assigned_seller = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(role='seller'),
        required=False,
        allow_null=True
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=False,
        allow_null=True
    )
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'role', 'first_name', 'last_name',
            'email', 'profile_image', 'phone_number', 'assigned_seller',
            'city', 'discount_percentage'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserProfile(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


User = get_user_model()

class SignedInUserSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)  # Assuming City model has 'name'

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'city_name',
            'profile_image',
        ]





class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']
        read_only_fields = ['id']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'email', 'city']
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.role = 'seller'
        user.save()
        return user
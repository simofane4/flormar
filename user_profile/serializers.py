
# Add your serializers here 
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

UserProfile = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'role',
            'first_name',
            'last_name',
            'email',
            'profile_image',
            'phone_number',
            'assigned_seller',
            'city',
        ]
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True},
            'phone_number': {'required': True, 'allow_blank': False},  # Enforce phone number
        }

    def validate_phone_number(self, value):
        """
        Check that the phone number is unique.
        """
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def create(self, validated_data):
        """
        Custom create method to handle user creation.
        """
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom update method.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.role = validated_data.get('role', instance.role)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.assigned_seller = validated_data.get('assigned_seller', instance.assigned_seller)
        instance.city = validated_data.get('city', instance.city)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)

        instance.save()
        return instance


User = get_user_model()

class SignedInUserSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)  # Assuming City model has 'name'

    class Meta:
        model = User
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
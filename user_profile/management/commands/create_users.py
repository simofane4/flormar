import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from faker import Faker
from user_profile.models import UserProfile, City

class Command(BaseCommand):
    help = 'Generates 100 fake users with random data'

    def handle(self, *args, **options):
        fake = Faker()

        # Fetch the admin user (make sure the admin user exists)
        try:
            admin_user = get_user_model().objects.get(role='admin')  # Replace 'admin' with the correct username
        except get_user_model().DoesNotExist:
            raise ValueError("Admin user with username 'admin' does not exist. Please create one.")

        # Fetch cities and sellers
        cities = list(City.objects.all())
        sellers = list(get_user_model().objects.filter(role='seller'))  # Assuming 'seller' role exists
        roles = ["client", "seller", "admin"]  # Replace with actual roles from UserRole.choices if needed

        for i in range(1, 101):
            while True:  # Retry if unique constraint fails
                try:
                    role = fake.random_element(roles)  # Random role selection

                    # Generate a unique 10-digit phone number starting with "06"
                    phone_number = f"06{fake.random_number(digits=8, fix_len=True)}"

                    # Create the user
                    user = UserProfile.objects.create(
                        username=f"user{i}",
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.unique.email(),  # Ensures email uniqueness
                        role=role,
                        profile_image=None,
                        phone_number=phone_number,
                        assigned_seller=fake.random_element(sellers) if sellers and role == "client" else None,
                        city=fake.random_element(cities) if cities else None,
                        created_by=admin_user,
                        updated_by=None
                    )
                    # Set the password for the user
                    user.password = make_password(f"password{i}")  # Example: password1, password2...
                    user.save()

                    self.stdout.write(self.style.SUCCESS(f"User {i} created successfully: {user.username}"))
                    break  # Exit the loop if creation succeeds
                except IntegrityError as e:
                    self.stdout.write(self.style.WARNING(f"Duplicate entry found. Retrying... ({str(e)})"))
                    fake.unique.clear()  # Clear the uniqueness cache to retry

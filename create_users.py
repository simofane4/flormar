import os
import django
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from faker import Faker
from user_profile.models import UserProfile, City
from django.contrib.auth import get_user_model

# Set the environment variable to point to your settings 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flormar.settings')  # Update to the correct path if needed

# Initialize Django
django.setup()

# Get the custom user model
User = get_user_model()

fake = Faker()

# Fetch the admin user (make sure the admin user exists)
try:
    admin_user = User.objects.get(username='admin')  # Replace 'admin' with an appropriate username
except User.DoesNotExist:
    raise ValueError("Admin user with username 'admin' does not exist. Please create one.")

# Fetch cities and sellers
cities = list(City.objects.all())
sellers = list(User.objects.filter(role='seller'))  # Assuming 'seller' role exists
roles = ["client", "seller", "admin"]  # Replace with actual roles from UserRole.choices if needed

# Generate users
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
            print(f"User {i} created successfully: {user.username}")
            break  # Exit the loop if creation succeeds
        except IntegrityError as e:
            print(f"Duplicate entry found. Retrying... ({str(e)})")
            fake.unique.clear()  # Clear the uniqueness cache to retry

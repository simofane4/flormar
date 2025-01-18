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



"""

    path('admin/', admin.site.urls),
    path('api/auth/', include('user_profile.urls')), # auth
    path('api/', include('products.urls')), # Product 
    path('api/', include('cart.urls')), # cart 
    path('api/', include('order.urls')), # Proorderduct 
    path('api/', include('checkout.urls')), # checkout 
        # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Products
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Product Images
    path('product-images/', ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('product-images/<int:pk>/', ProductImageDetailView.as_view(), name='product-image-detail'),
    
    # Product Variations
    path('product-variations/', ProductVariationListCreateView.as_view(), name='product-variation-list-create'),
    path('product-variations/<int:pk>/', ProductVariationDetailView.as_view(), name='product-variation-detail'),
    
    # Custom Views
    path('popular-products/', PopularProductsView.as_view(), name='popular-products'),
    path('categories/<int:category_id>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
    path("sign-in-with-token/", SignInWithTokenView.as_view(), name="sign-in-with-token"),
    path('me/', SignedInUserView.as_view(), name='signed-in-user'),
    path('orders/', views.list_orders, name='order-list'),
    path('order/<int:order_id>/', views.view_order, name='order-detail'),
    path('order/create/', views.create_order, name='order-create'),
    path('order/update-status/<int:order_id>/', views.update_order_status, name='order-update-status'),
    path('order/delete/<int:order_id>/', views.delete_order, name='order-delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-payment-status/<int:order_id>/', views.update_payment_status, name='update-payment-status'),
    path('cart/', CartView.as_view(), name='cart-view'),  # View the cart
    path('cart/add/', AddCartItemView.as_view(), name='add-to-cart'),  # Add item to cart
    path('cart/update/', UpdateCartItemView.as_view(), name='update-cart-item'),  # Update item quantity
    path('cart/remove/', RemoveCartItemView.as_view(), name='remove-from-cart'),  # Remove item from cart
    path('cart/clear/', ClearCartView.as_view(), name='clear-cart'),  # Clear the cart

"""
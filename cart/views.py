from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartView(generics.RetrieveAPIView):
    """
    View to retrieve the cart of the current logged-in user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.objects.get(client=self.request.user)

class AddCartItemView(generics.CreateAPIView):
    """
    Add a product to the user's cart.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        cart, created = Cart.objects.get_or_create(client=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        # If the item already exists in the cart, increase the quantity
        if not created:
            cart_item.quantity += int(self.request.data['quantity'])
            cart_item.save()

        serializer.save(cart=cart)

    def create(self, request, *args, **kwargs):
        if 'product' not in request.data or 'quantity' not in request.data:
            return Response({"detail": "Product and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class UpdateCartItemView(generics.UpdateAPIView):
    """
    Update the quantity of a product in the user's cart.
    """
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_update(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        cart_item = CartItem.objects.get(cart=self.request.user.cart, product=product)
        cart_item.quantity = self.request.data['quantity']
        cart_item.save()
        serializer.save()

class RemoveCartItemView(generics.DestroyAPIView):
    """
    Remove a product from the user's cart.
    """
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_destroy(self, instance):
        instance.delete()

class ClearCartView(generics.DestroyAPIView):
    """
    Clear all items from the user's cart.
    """
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        cart = Cart.objects.get(client=self.request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

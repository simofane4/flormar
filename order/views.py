# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from cart.models import Cart
from .serializers import OrderSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Create Order - Only sellers can create an order for a client
@api_view(['POST'])
def create_order(request):
    if request.user.role != 'seller':
        return Response({"detail": "You do not have permission to create orders."}, status=status.HTTP_403_FORBIDDEN)

    client_id = request.data.get('client_id')
    client = get_object_or_404(User, pk=client_id)
    cart = get_object_or_404(Cart, client=client)

    # Create the order
    order = Order.objects.create(
        client=client,
        seller=request.user,
        cart=cart,
        status='pending',
    )

    return Response({"detail": f"Order {order.id} created successfully."}, status=status.HTTP_201_CREATED)

# List Orders - Only admins and sellers can list orders
@api_view(['GET'])
def list_orders(request):
    if request.user.role not in ['admin', 'seller']:
        return Response({"detail": "You do not have permission to view orders."}, status=status.HTTP_403_FORBIDDEN)

    if request.user.role == 'admin':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(seller=request.user)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# View Order Detail - View the details of a specific order
@api_view(['GET'])
def view_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Only the seller of the order, the client, or an admin can view the order
    if request.user != order.seller and request.user != order.client and request.user.role != 'admin':
        return Response({"detail": "You do not have permission to view this order."}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

# Update Order Status - Sellers or admins can update the order status
@api_view(['PUT'])
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.user.role not in ['admin', 'seller']:
        return Response({"detail": "You do not have permission to update the order."}, status=status.HTTP_403_FORBIDDEN)

    # Updating the order status
    new_status = request.data.get('status', order.status)
    if new_status not in ['pending', 'confirmed']:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()

    return Response({"detail": "Order status updated successfully."}, status=status.HTTP_200_OK)

# Delete Order - Admins can delete orders
@api_view(['DELETE'])
def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.user.role != 'admin':
        return Response({"detail": "You do not have permission to delete this order."}, status=status.HTTP_403_FORBIDDEN)

    order.delete()
    return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

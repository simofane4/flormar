from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from order.models import Order, PaymentMethod, PaymentStatus
from cart.models import Cart
from django.contrib.auth import get_user_model
from .serializers import OrderSerializer

User = get_user_model()

@api_view(['POST'])
def checkout(request):
    client = request.user
    payment_method = request.data.get('payment_method')  # cash or check
    cart = Cart.objects.get(client=client)

    # Create the order
    order = Order.objects.create(
        client=client,
        seller=cart.seller,  # Assuming cart has the seller
        cart=cart,
        payment_method=payment_method,
        payment_status=PaymentStatus.PENDING if payment_method == PaymentMethod.CASH else PaymentStatus.CHECK_PENDING,
    )

    return Response({"detail": f"Order {order.id} created successfully."}, status=status.HTTP_201_CREATED)



@api_view(['PUT'])
def update_payment_status(request, order_id):
    order = Order.objects.get(id=order_id)

    # Only the seller or admin can update payment status
    if request.user != order.seller and request.user.role != 'admin':
        return Response({"detail": "You do not have permission to update the payment status."}, status=status.HTTP_403_FORBIDDEN)

    new_status = request.data.get('payment_status')
    if new_status not in PaymentStatus.values:
        return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    # Update the payment status
    order.payment_status = new_status
    order.save()

    return Response({"detail": f"Payment status updated to {new_status}."}, status=status.HTTP_200_OK)
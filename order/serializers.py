
# Add your serializers here 

from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'seller', 'cart', 'payment_method', 'payment_status', 'status', 'created_at', 'updated_at']
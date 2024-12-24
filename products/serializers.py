from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'parent', 'created', 'modified']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'product', 'attribute_name', 'attribute_value', 'additional_price', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  # Nested ProductImage
    variations = ProductVariationSerializer(many=True, read_only=True)  # Nested ProductVariation
    category_name = serializers.CharField(source="category.name", read_only=True)  # Additional field

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'title', 'price', 'image', 
            'description', 'quantity', 'views', 'is_deleted', 'barcode', 'sku',
            'images', 'variations'
        ]

from rest_framework import generics, filters
from .models import Category, Product, ProductImage, ProductVariation
from .serializers import CategorySerializer, ProductImageSerializer, ProductSerializer, ProductVariationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# List and Create Categories
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Retrieve, Update, and Delete a Category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# List and Create Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.prefetch_related('images', 'variations').all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


# Retrieve, Update, and Delete a Product
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.prefetch_related('images', 'variations').all()
    serializer_class = ProductSerializer


# List and Create Product Images
class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.select_related('product').all()
    serializer_class = ProductImageSerializer

# Retrieve, Update, and Delete a Product Image
class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.select_related('product').all()
    serializer_class = ProductImageSerializer


# List and Create Product Variations
class ProductVariationListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariation.objects.select_related('product').all()
    serializer_class = ProductVariationSerializer

# Retrieve, Update, and Delete a Product Variation
class ProductVariationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariation.objects.select_related('product').all()
    serializer_class = ProductVariationSerializer

# Custom Views
class SearchProductsView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        products = Product.objects.filter(title__icontains=query, is_deleted=False)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    
class PopularProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_deleted=False).order_by('-views')[:10]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductsByCategoryView(APIView):
    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id, is_deleted=False)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ProductListCreateView, ProductDetailView,
    ProductImageListCreateView, ProductImageDetailView,
    ProductVariationListCreateView, ProductVariationDetailView,
    PopularProductsView, ProductsByCategoryView,
)

urlpatterns = [
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
]

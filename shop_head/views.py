from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from .models import (Category, Product, Image, 
                     Order, OrderedProduct, Comment
                     )
from .serializers import (CategorySerializer, ProductSerializer, 
                          ImageSerializer, OrderSerializer, 
                          OrderedProductSerializer, CommentSerializer,
                          ProductDetailSerializer)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.cache import cache
from rest_framework.response import Response

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        return obj.user == request.user

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryProductsAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('images', 'comments')

    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderedProductViewSet(ModelViewSet):
    queryset = OrderedProduct.objects.all()
    serializer_class = OrderedProductSerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if product_id:
            return Comment.objects.filter(product_id=product_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryListAPIView(APIView):
    def get(self, request):
        data = cache.get('categories')
        if not data:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            data = serializer.data
            cache.set('categories', data, timeout=30)
        return Response(data)

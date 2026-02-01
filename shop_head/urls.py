from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, CategoryProductsAPIView, 
                    ProductViewSet, ImageViewSet,
                    OrderViewSet, OrderedProductViewSet,
                    CommentViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register(r'images', ImageViewSet, basename='image')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderedProductViewSet, basename='order-item')
router.register(r'comments', CommentViewSet, basename='comment')



urlpatterns = [
    path('', include(router.urls)),
    path('categories/<int:category_id>/products/', CategoryProductsAPIView.as_view(), name='category-products'),
]

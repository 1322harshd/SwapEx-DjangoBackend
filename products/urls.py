from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, FavoriteViewSet, update_product_and_deactivate, record_product_sale

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
	path('products/<int:pk>/custom-update/', update_product_and_deactivate, name='custom-product-update'),
	path('products/record-sale/', record_product_sale, name='record-product-sale'),
	path('', include(router.urls)),
]

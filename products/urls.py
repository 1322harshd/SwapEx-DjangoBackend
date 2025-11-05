from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = router.urls
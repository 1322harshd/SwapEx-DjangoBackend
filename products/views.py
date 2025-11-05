from django.shortcuts import render
from rest_framework import viewsets, permissions, parsers
from .models import Product, Favorite
from .serializers import ProductSerializer, FavoriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

# method to give permissions to seller and buyer it returns True if request is made by seller and False if it is made by buyer
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user
#Viewset for product model
class ProductViewSet(viewsets.ModelViewSet):#using ModelViewSet which handles all basic endpoints
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]#adding permission classes
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]#adding filters
    filterset_fields = ['condition', 'category']           
    ordering_fields = ['price', 'created_at']              
    search_fields = ['title', 'description']               
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]  # allow file uploads
 
#custom query method to get seller info and not getting products listed by logged in user
    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('seller')
        print("DEBUG user:", getattr(self.request, "user", None), "qs_before:", qs.count())
        if self.action == 'list' and self.request.user and self.request.user.is_authenticated:
            qs = qs.exclude(seller=self.request.user)
            print("DEBUG excluded own, qs_after:", qs.count())
        return qs
    #method to set logged in user as seller when product posted
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
 
    #debug helper
    def create(self, request, *args, **kwargs):
        print("REQUEST DATA:", request.data)   # DEBUG: shows parsed multipart data
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        """Return products listed by the current user."""
        products = Product.objects.filter(seller=request.user, is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('product')
 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 
    def destroy(self, request, *args, **kwargs):
        fav = self.get_object()
        if fav.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
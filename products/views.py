from django.shortcuts import render
from rest_framework import viewsets, permissions, parsers
from .models import Product, Favorite
from .serializers import ProductSerializer, FavoriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('seller')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['condition', 'category']            # allow ?category=...&condition=...
    ordering_fields = ['price', 'created_at']              # allow ?ordering=price or ?ordering=-price
    search_fields = ['title', 'description']               # allow ?search=keyword
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]  # allow file uploads

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('seller')
        print("DEBUG user:", getattr(self.request, "user", None), "qs_before:", qs.count())
        if self.action == 'list' and self.request.user and self.request.user.is_authenticated:
            qs = qs.exclude(seller=self.request.user)
            print("DEBUG excluded own, qs_after:", qs.count())
        return qs

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    # optional debug helper
    def create(self, request, *args, **kwargs):
        print("REQUEST DATA:", request.data)   # DEBUG: shows parsed multipart data
        return super().create(request, *args, **kwargs)

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

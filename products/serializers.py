from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)
    primary_image = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Product
        fields = ('id', 'seller', 'title', 'category', 'description', 'price', 'condition',
                  'is_active', 'primary_image', 'created_at', 'updated_at')
        read_only_fields = ('id', 'seller', 'created_at', 'updated_at')
from rest_framework import serializers
from .models import Product, Favorite

class ProductSerializer(serializers.ModelSerializer):
    # Add seller information to the product response
    seller_name = serializers.CharField(source='seller.first_name', read_only=True)
    seller_email = serializers.EmailField(source='seller.email', read_only=True)
    seller_full_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'seller_name', 'seller_email', 'seller_full_name',
            'title', 'category', 'description', 'price', 'condition',
            'brand', 'model_name', 'is_active', 'is_available', 
            'primary_image', 'image_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'seller', 'created_at', 'updated_at')

    def get_seller_full_name(self, obj):
        """Get seller's full name"""
        return f"{obj.seller.first_name} {obj.seller.last_name}".strip()

    def get_image_url(self, obj):
        """Get absolute URL for the image"""
        if obj.primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.primary_image.url)
        return None

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='product', queryset=ProductSerializer.Meta.model.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'product', 'created_at']
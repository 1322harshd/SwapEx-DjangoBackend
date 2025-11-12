from rest_framework import serializers
from .models import Product,Favorite
from authentication.serializers import SellerPublicSerializer  # import the public seller serializer

#serializer class definition
class ProductSerializer(serializers.ModelSerializer):#using ModelSerializer which automatically maps model fields and serializer feilds
    seller = SellerPublicSerializer(read_only=True)   # nested seller object
    #serializing image field
    primary_image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    
    #method to link serializer to product model
    class Meta:
        model = Product
        fields = ('id', 'seller', 'title', 'category', 'description', 'price', 'condition',
                  'is_active', 'primary_image', 'created_at', 'updated_at', 'is_sold', 'is_available')
        
        read_only_fields = ('id', 'seller', 'created_at', 'updated_at')

# FavoriteSerializer manages serialization for the Favorite model.
# It allows users to favorite products and view their favorite list.
class FavoriteSerializer(serializers.ModelSerializer):
    # Shows the full product details for each favorite (read-only).
    product = ProductSerializer(read_only=True)
    # Allows users to add a favorite by specifying the product's ID.
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='product', queryset=ProductSerializer.Meta.model.objects.all()
    )
 
    class Meta:
        model = Favorite
        # Fields exposed in the API for favorites.
        fields = ['id', 'product', 'product_id', 'created_at']
        # These fields are read-only and cannot be set by the client.
        read_only_fields = ['id', 'product', 'created_at']

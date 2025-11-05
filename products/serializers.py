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
                  'is_active', 'primary_image', 'created_at', 'updated_at')
        #fields that cannot be edited
        read_only_fields = ('id', 'seller', 'created_at', 'updated_at')

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='product', queryset=ProductSerializer.Meta.model.objects.all()
    )
 
    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'product', 'created_at']
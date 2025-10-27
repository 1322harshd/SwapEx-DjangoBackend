from rest_framework import serializers
from .models import Product
#serializer class definition
class ProductSerializer(serializers.ModelSerializer):#using ModelSerializer which automatically maps model fields and serializer feilds
    seller = serializers.StringRelatedField(read_only=True)
    #serializing image field
    primary_image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    
    #method to link serializer to product model
    class Meta:
        model = Product
        fields = ('id', 'seller', 'title', 'category', 'description', 'price', 'condition',
                  'is_active', 'primary_image', 'created_at', 'updated_at')
        #fields that cannot be edited
        read_only_fields = ('id', 'seller', 'created_at', 'updated_at')
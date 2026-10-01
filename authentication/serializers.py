from rest_framework import serializers
from .models import Student

class StudentSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)#avoids sending password back as response

    class Meta:
        model = Student
        fields = ['first_name', 'email', 'phone_number', 'password', 'profile_image', 'student_id_image']

    def create(self, validated_data):#method to hash password and set "is_approved" field to False and save it
        password = validated_data.pop('password')
        user = Student(**validated_data)
        user.set_password(password)
        user.is_approved = False  
        user.save()
        return user

# public serializer for seller info (safe fields only)
class SellerPublicSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ("id", "first_name", "email", "phone_number", "profile_image", "trust_badge", "joined_at")
        read_only_fields = fields
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            # This will return the full S3 URL
            return obj.profile_image.url
        return None

class StudentProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'email', 'phone_number', 'profile_image', 'trust_badge', 'joined_at']
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            # This will return the full S3 URL when S3 storage is configured
            return obj.profile_image.url
        return None
    
    def update(self, instance, validated_data):
        # Handle profile image updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


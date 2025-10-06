from rest_framework import serializers
from .models import Student

class StudentSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['username', 'email', 'phone_number', 'password', 'profile_image', 'student_id_image']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Student(**validated_data)
        user.set_password(password)
        user.is_approved = False  
        user.save()
        return user
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
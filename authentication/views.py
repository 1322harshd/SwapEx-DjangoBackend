from django.shortcuts import render
from rest_framework import generics
from .models import Student
from .serializers import StudentSignUpSerializer

# Create your views here.

class StudentSignUpView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSignUpSerializer

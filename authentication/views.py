from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import Student
from .serializers import StudentSignUpSerializer
from rest_framework.decorators import api_view





class StudentSignUpView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSignUpSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("CustomTokenObtainPairView called")  
        
        # Get email/username and password from request
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"Email: {email}") 
        print(f"Password provided: {password is not None}")  
        
        try:
            # Check if student exists
            student = Student.objects.get(email=email)
            print(f"Student found: {student.email}, is_approved: {student.is_approved}")  
            
            # Check if student is approved
            if not student.is_approved:
                print("Student not approved") 
                return Response(
                    {'error': 'Account is not approved yet.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check password
            if not student.check_password(password):
                print("Password check failed") 
                return Response(
                    {'error': 'Invalid credentials.'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            print("All checks passed, proceeding with token generation")  
                
        except Student.DoesNotExist:
            print("Student does not exist") 
            return Response(
                {'error': 'Invalid credentials.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # If all checks pass, proceed with normal token generation
        return super().post(request, *args, **kwargs)


@api_view(['POST'])
def forgot_password_view(request):
    """Reset password - checks if email exists and updates password"""
    email = request.data.get('email')
    new_password = request.data.get('new_password')
    
    print(f"🔍 Password reset attempt for: {email}")
    
    # Validate input
    if not email or not new_password:
        return Response({
            'message': 'Email and new password are required.',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 6:
        return Response({
            'message': 'Password must be at least 6 characters long.',
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check if user exists in database
        student = Student.objects.get(email=email)
        
        print(f"✅ User found: {email}")
        
        # Update password (this will hash it properly)
        student.set_password(new_password)
        student.save()
        
        print(f"✅ Password updated successfully for: {email}")
        
        return Response({
            'message': 'Password updated successfully! You can now login with your new password.',
            'status': 'success'
        }, status=status.HTTP_200_OK)
        
    except Student.DoesNotExist:
        print(f"❌ User not found: {email}")
        return Response({
            'message': 'No account found with this email address. Please enter the correct email ID to update password.',
            'status': 'user_not_found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print(f"❌ Error updating password: {str(e)}")
        return Response({
            'message': 'An error occurred while updating password. Please try again.',
            'status': 'error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
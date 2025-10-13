from django.urls import path
from .views import StudentSignUpView, CustomTokenObtainPairView, forgot_password_view

urlpatterns = [
    path('signup/', StudentSignUpView.as_view(), name='student-signup'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),  
]


    
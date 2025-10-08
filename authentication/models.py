from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)  # Make email required and unique
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', blank=True, null=True)
    student_id_image = models.ImageField(upload_to='id_images/', blank=True, null=True)
    trust_badge = models.IntegerField(default=0)
    wallet_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add other required fields if needed

class SignupRequest(Student):
    class Meta:
        proxy = True
        verbose_name = "Signup Request"
        verbose_name_plural = "Signup Requests"




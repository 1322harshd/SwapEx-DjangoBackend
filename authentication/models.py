from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Student(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)  # Make username null
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', blank=True, null=True)
    student_id_image = models.ImageField(upload_to='id_images/', blank=True, null=True)
    trust_badge = models.IntegerField(default=0)
    wallet_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def save(self, *args, **kwargs):
        # Set username to email for consistency, or make it None
        if self.email:
            self.username = self.email
        super().save(*args, **kwargs)

class SignupRequest(Student):
    class Meta:
        proxy = True
        verbose_name = "Signup Request"
        verbose_name_plural = "Signup Requests"




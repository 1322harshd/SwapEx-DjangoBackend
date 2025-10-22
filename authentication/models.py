from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# custom user manager 
class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):#for students
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):#for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Student(AbstractUser):#custom user model
    username = models.CharField(max_length=150, unique=True, null=True, blank=True) 
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpeg', blank=True, null=True)
    student_id_image = models.ImageField(upload_to='id_images/', blank=True, null=True)
    trust_badge = models.IntegerField(default=0)
    wallet_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()#override of default user model so that we can use our custom ones (create_user and create_superuser)

    USERNAME_FIELD = 'email'#sets email as required field to login instead of username
    REQUIRED_FIELDS = []  

    def save(self, *args, **kwargs):
        #function to set username as email 
        if self.email:
            self.username = self.email
        super().save(*args, **kwargs)

class SignupRequest(Student):#proxy model to show signup requests in admin panel
    class Meta:
        proxy = True
        verbose_name = "Signup Request"
        verbose_name_plural = "Signup Requests"




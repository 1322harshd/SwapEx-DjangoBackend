from django.db import models
from django.conf import settings
from django.db import models

#model for products
class Product(models.Model):
    class Condition(models.TextChoices):
        NEW = 'new', 'New'
        LIKE_NEW = 'used_like_new', 'Used - Like New'
        GOOD = 'used_good', 'Used - Good'
        FAIR = 'used_fair', 'Used - Fair'
   
    title = models.CharField(max_length=255)

    #linking to seller from Student model in authentication app
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    category = models.CharField(max_length=100, blank=True, null=True)  
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.NEW)
    is_active = models.BooleanField(default=True)
    primary_image = models.ImageField(upload_to='products/primary/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #method to call new products first 
    class Meta:
        ordering = ['-created_at']
    
    #method to make string representation
    def __str__(self):
        return f"{self.title} — {self.seller.email}"

#proxy model for pending signup requests
class PendingProduct(Product):
    class Meta:
        proxy = True
        verbose_name = "Pending product"
        verbose_name_plural = "Pending products"



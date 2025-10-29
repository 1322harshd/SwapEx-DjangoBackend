from django.db import models
from django.conf import settings

class Product(models.Model):
    class Condition(models.TextChoices):
        NEW = 'new', 'New'
        LIKE_NEW = 'used_like_new', 'Used - Like New'
        GOOD = 'used_good', 'Used - Good'
        FAIR = 'used_fair', 'Used - Fair'

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.NEW)
    is_active = models.BooleanField(default=True)
    primary_image = models.ImageField(upload_to='products/primary/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.seller.email}"

class PendingProduct(Product):
    class Meta:
        proxy = True
        verbose_name = "Pending product"
        verbose_name_plural = "Pending products"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} -> {self.product}"



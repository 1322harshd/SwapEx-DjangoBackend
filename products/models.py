from django.db import models
from django.conf import settings

#model for products
class Product(models.Model):
    # Enum for product condition, making it easy to select and display quality.
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
    brand = models.CharField(max_length=100, blank=True, null=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False) 

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

# Favorite model allows users to mark products as favorites for quick access.
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    # Ensure a user can only favorite a product once.
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} -> {self.product}"

# ProductSaleTransaction records each sale, linking the product, buyer, and sale details.
class ProductSaleTransaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_transactions')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.product.title} to {self.buyer.email} for {self.amount} on {self.timestamp}"



from django.contrib import admin
from django.utils.html import mark_safe
from .models import Product, PendingProduct, ProductSaleTransaction 

# ProductAdmin manages how Product objects appear in the Django admin.
# It provides custom list display, filtering, searching, and bulk actions for product approval/rejection.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'price', 'condition', 'brand', 'manufacture_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'condition', 'category', 'brand', 'manufacture_date')
    search_fields = ('title', 'description', 'seller__email')
    readonly_fields = ('primary_image_link', 'created_at', 'updated_at')
    fields = ('seller', 'title', 'category', 'description', 'price', 'condition', 'brand', 'manufacture_date', 'is_active',
              'primary_image_link', 'created_at', 'updated_at')
    actions = ['approve_products', 'reject_products']

    #method for preview of image
    def primary_image_link(self, obj):
        if obj.primary_image:
            return mark_safe(
                f'<a href="{obj.primary_image.url}" target="_blank">'
                f'<img src="{obj.primary_image.url}" style="max-height:120px;"/></a>'
            )
        return "No image"
    primary_image_link.short_description = "Primary image"
    
    #  action to approve selected products (sets is_active to True).
    def approve_products(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, f"{updated} product(s) approved.")
    approve_products.short_description = "Approve selected products"
 
    #  action for to reject (delete) selected products.
    def reject_products(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} product(s) rejected and removed.")
    reject_products.short_description = "Reject selected products (delete)"

    # Automatically set is_available to True when a product is approved (is_active=True).
    # This keeps the admin interface simple and ensures approved products are available.
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.is_available = True
        super().save_model(request, obj, form, change)

# PendingProductAdmin is a proxy for managing products that are awaiting approval.
# Only shows products that are not yet active, and provides custom actions for approval/rejection.
@admin.register(PendingProduct)
class PendingProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'price', 'condition', 'brand', 'manufacture_date', 'is_active', 'created_at')
    list_filter = ('condition', 'category', 'brand', 'manufacture_date')
    search_fields = ('title', 'description', 'seller__email')
    readonly_fields = ('primary_image_link', 'created_at', 'updated_at')
    # include is_active so admin can toggle approval on the product detail form
    fields = ('seller', 'title', 'category', 'description', 'price', 'condition', 'brand', 'manufacture_date', 'is_active', 'primary_image_link', 'created_at', 'updated_at')
    actions = ['approve_pending', 'reject_pending']

    # Only show products that are not active (pending approval).
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=False)

    # Show image preview for pending products.
    def primary_image_link(self, obj):
        if obj.primary_image:
            return mark_safe(
                f'<a href="{obj.primary_image.url}" target="_blank">'
                f'<img src="{obj.primary_image.url}" style="max-height:120px;"/></a>'
            )
        return "No image"
    primary_image_link.short_description = "Primary image"

    # Delegate permissions to the real Product model for consistency.
    def has_add_permission(self, request):
        return request.user.has_perm('products.add_product') or super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('products.change_product') or super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('products.delete_product') or super().has_delete_permission(request, obj)
    
    #method to approve the product
    def approve_pending(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} product(s) approved.")
    approve_pending.short_description = "Approve selected pending products"

    # method to reject the product
    def reject_pending(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} product(s) rejected and removed.")
    reject_pending.short_description = "Reject selected pending products (delete)"

# ProductSaleTransactionAdmin manages sale transaction records in the admin.
# Allows filtering and searching by product and buyer for easy lookup.
@admin.register(ProductSaleTransaction)
class ProductSaleTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'amount', 'timestamp')
    list_filter = ('product', 'buyer')
    search_fields = ('product__title', 'buyer__email')

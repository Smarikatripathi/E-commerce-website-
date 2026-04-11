from django.contrib import admin
from core.models import (
    Category, Vendor, Product, ProductImage,
     Wishlist, ProductReview, Address, HeroSlide, Order, OrderItem, Payment,
)

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1


class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order')
    list_filter = ('active',)
    list_editable = ('active', 'order')


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = (
        'user', 'title', 'product_image',
        'price', 'in_stock', 'product_status',
        'date','pid',
    )
    list_filter = ('in_stock', 'product_status', 'date')
    search_fields = ('title', 'description')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')
    search_fields = ('title',)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'address')
    search_fields = ('title', 'phone')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__title',)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'payment_status', 'paid_status', 'created_at')
    list_filter = ('payment_status', 'paid_status')


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'date')
    search_fields = ('user__username', 'product__title')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'address_line1', 'city',
        'state', 'postal_code', 'country'
    )

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'amount', 'status', 'created_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(HeroSlide, HeroSlideAdmin)
admin.site.register(Payment, PaymentAdmin)

from django.contrib import admin
from core.models import (
    Category, Vendor, Product, ProductImage,
    CartOrderItem, CartOrderItems,
    Tags, Wishlist, ProductReview, Address, HeroSlide
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
        'date', 'updated','pid','deal_end'
    )
    list_filter = ('in_stock', 'product_status', 'date')
    search_fields = ('title', 'description')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')
    search_fields = ('title',)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'address')
    search_fields = ('title', 'phone')


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'price', 'paid_status',
        'product_status', 'ordered_date'
    )
    list_filter = ('paid_status', 'product_status')


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'invoice_no', 'item',
        'quantity', 'price'
    )
    search_fields = ('invoice_no', 'item')


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(HeroSlide, HeroSlideAdmin)



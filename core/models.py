from django.db import models
from django.utils.html import mark_safe
from django.conf import settings
import uuid

from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


# CHOICES
STATUS_CHOICES = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

RATING = (
    ('1', '⭐'),
    ('2', '⭐⭐'),
    ('3', '⭐⭐⭐'),
    ('4', '⭐⭐⭐⭐'),
    ('5', '⭐⭐⭐⭐⭐'),
)

# CATEGORY
class Category(models.Model):
    cid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to='categories/', default='categories/default.jpg')

    def __str__(self):
        return self.title

    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
# VENDOR
class Vendor(models.Model):
    vid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100, default="Best Vendor")
    image = models.ImageField(upload_to='vendors/')
    description = RichTextUploadingField(null=True, blank=True)

    address = models.CharField(max_length=255, default="123 Main street")
    phone = models.CharField(max_length=20, default="+1234567890")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    

# PRODUCT
class Product(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    title = models.CharField(max_length=100, default="Fresh pear")
    image = models.ImageField(upload_to='products/', default='products/default.jpg')
    description = RichTextUploadingField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=100, default="in_review")

    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

# PRODUCT IMAGE
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    date = models.DateTimeField(auto_now_add=True)

# PRODUCT REVIEW
class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField(null=True, blank=True)
    rating = models.CharField(choices=RATING, max_length=10, default="3")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


# WISHLIST

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


# ADDRESS
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# HERO SLIDER
class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='hero_slides/')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


#  ORDER SYSTEM (FINAL CLEAN VERSION)

# ORDER (PARENT)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_status = models.CharField(
    max_length=20,
    choices=(
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ),
    default='pending'
)

    paid_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# ORDER ITEM (CHILD)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"    

# PAYMENT
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=50, default="khalti")
    transaction_id = models.CharField(max_length=200, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ),
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
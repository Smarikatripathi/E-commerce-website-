from django.db import models
from django.utils.html import mark_safe
from django.utils import timezone
from userauths.models import User
from django.conf import settings
import uuid
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

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

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Category(models.Model):
    cid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100,default="Food")
    image = models.ImageField(upload_to='categories/',default='categories/default.jpg')
    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image.url))        

    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass    

class Vendor(models.Model):
    vid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    title = models.CharField(max_length=100,default="Best Vendor")
    image = models.ImageField(upload_to='vendors/')
    description = RichTextUploadingField(null=True, blank=True,default="Best vendor in town")

    address = models.CharField(max_length=255, default="123 Main street")
    phone = models.CharField(max_length=20, default="+123 (456) 789-0000")
    chat_response_time = models.CharField(max_length=50, default="1 hour")
    shipping_on_time = models.CharField(max_length=50, default="24 hours")
    authentic_rating = models.CharField(max_length=50, default="99%")
    days_return = models.CharField(max_length=50, default="7 days")
    warranty = models.CharField(max_length=50, default="No warranty")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image.url))        

    def __str__(self):
        return self.title

class Product(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('category', on_delete=models.SET_NULL, null=True, blank=True,related_name='products')
    vendor = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True, blank=True,related_name='products')
    
    title = models.CharField(max_length=100,default="Fresh pear")
    image = models.ImageField(upload_to='products/',default='products/default.jpg')
    description = RichTextUploadingField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    old_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    specifications = RichTextUploadingField(null=True, blank=True,default="Product specifications here")
    type = models.CharField(max_length=100, default="General",null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="100",null=True, blank=True)
    life = models.CharField(max_length=100, default="7 days",null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    exp = models.DateTimeField(null=True, blank=True)

    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=100, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    deal_end = models.DateTimeField(null=True, blank=True)
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe(f'<img src="%s" width="50" height="50" />'%(self.image.url))        

    def __str__(self):
        return self.title
    
    def get_percentage(self):
        if self.old_price > 0:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return discount
        return 0

    
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

class CartOrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_status = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        default="process"
    )

    class Meta:
        verbose_name = "Cart Order Item"
        verbose_name_plural = "Cart Order Items"


class CartOrderItems(models.Model):
    order = models.ForeignKey('CartOrderItem', on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=100, blank=True)
    product_status = models.CharField( max_length=100)
    item = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

    class Meta:
        verbose_name = "Cart Order Items"
        verbose_name_plural = "Cart Order Items"  
  
    
    #product review model,wishlist model,
class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True,related_name='reviews')
    review = models.TextField(null=True, blank=True)
    rating = models.CharField(choices=RATING, max_length=10, default="None")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.title}"
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.title}"
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"Address of {self.user.username}"
    
class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='hero_slides/')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title  
from itertools import product
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class DeliveryInformation(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=150, verbose_name="Recipient's Fullname", blank=False) 
    phone_number = models.CharField(max_length=13, default="+63", verbose_name="Phone Number", blank=False)
    telephone_number = models.CharField(max_length=12, default="(062)", verbose_name="Telephone Number", blank=True)
    barangay = models.CharField(max_length=150, verbose_name="Barangay", blank=False)
    landmark = models.CharField(max_length=150, verbose_name="Landmark", blank=False)
    street_name = models.CharField(max_length=150, verbose_name="House/Unit/Flr #, Bldg Name, Blk or Lot #", blank=False)
    city = models.CharField(max_length=150, verbose_name="City", default="Zamboanga City", blank=False)

    def __str__(self):
        return self.landmark

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price

class Favorites(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Customer Favorites'

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    address = models.ForeignKey(DeliveryInformation, verbose_name="Address", on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(verbose_name="Total Price")
    remarks = models.TextField(verbose_name="Remarks", blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
    )   

class OrderItem(models.Model):
    invoice_no=models.CharField(max_length=150)
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    price = models.DecimalField(max_digits=8, decimal_places=2) 

    @property
    def total_price(self):
        return self.quantity * self.product.price

class OrderRequest(models.Model):
    invoice_no=models.CharField(max_length=150)
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    file_upload = models.FileField()

class Reservation(models.Model):
    user = models.ForeignKey(User, verbose_name="User",on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, default="+63", verbose_name="Phone Number", blank=False)
    telephone_number = models.CharField(max_length=12, default="(062)", verbose_name="Telephone Number", blank=True)
    pax = models.PositiveIntegerField(verbose_name="Number of Guest", default=1, null=False)
    event_name = models.CharField(verbose_name="Event Name", max_length=150, null=False) 
    event_type = models.CharField(verbose_name="Event Type", max_length=150, null=False)
    event_date = models.DateField(verbose_name="Event Date")
    event_time = models.TimeField(verbose_name="Event Time", unique=True)
    event_time_end = models.TimeField(verbose_name="Event Time End", unique=True)
    remarks = models.TextField(verbose_name="Remarks", blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )

    def __str__(self):
        return self.event_name

class Gallery(models.Model):
    description = models.CharField(verbose_name="Description", max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery", blank=True, null=True, verbose_name="Gallery Image")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name_plural = "Gallery"

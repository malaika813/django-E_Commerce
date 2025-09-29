from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator





class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(default="https://via.placeholder.com/500")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    badge = models.CharField(max_length=20, choices=[('new', 'New'), ('sale', 'Sale')], null=True, blank=True)

    def __str__(self):
        return self.name

# ----------------- ORDER -----------------

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100, default="Unknown")
    phone = models.CharField(max_length=20, default="0000000000")
    address = models.TextField(default="Unknown")
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']  # ✅ newest orders first

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    

    
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('product', 'user')  # 1 review per user per product

    def __str__(self):
        return f"{self.product.name} - {self.rating}⭐ by {self.user.username}"


class OrderTracking(models.Model):
    order = models.ForeignKey("Order", related_name="tracking", on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # e.g. "Pending", "Shipped", "Delivered"
    note = models.TextField(blank=True)  # optional message like "Left warehouse"
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.order.id} - {self.status}"

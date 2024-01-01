from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Item(models.Model):
    UNIT_CHOICES = [
        ('', ''),
        ('unit', 'Unit'),
        ('stack', 'Stack'),
    ]

    STOCK_CHOICES = [
        ('in stock', 'IN STOCK'),
        ('low stock', 'LOW STOCK'),
        ('out of stock', 'OUT OF STOCK')
    ]

    CATEGORY_CHOICES = [
        ('armor and tools', 'Armor and Tools'),
        ('potions', 'Potions'),
        ('building blocks', 'Building Blocks'),
        ('food and farming', 'Food and Farming'),
        ('resources', 'Resources'),
        ('utility', 'Utility'),
        ('miscellaneous', 'Miscellaneous'),
    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(decimal_places=2, max_digits=6)
    description = models.TextField()
    quantity = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, null=True, blank=True)
    stock = models.CharField(max_length=20, choices=STOCK_CHOICES, default='out of stock')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='miscellaneous')

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Redeem(models.Model):
    code = models.CharField(max_length=50)
    diamonds = models.IntegerField()
    redeemed = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    x_coordinate = models.IntegerField()
    z_coordinate = models.IntegerField()
    cart_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    date_delivery = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"{self.user.username} - {self.date_created}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return Decimal(self.quantity) * self.item.price
    
    
class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

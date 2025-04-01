from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name="customer_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customer_permissions", blank=True)
    is_manager = models.BooleanField(default=False)
    is_delivery_crew = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_of_the_day = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.item_of_the_day:
            MenuItem.objects.filter(item_of_the_day=True).update(item_of_the_day=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="assigned_orders")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('delivered', 'Delivered')])
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
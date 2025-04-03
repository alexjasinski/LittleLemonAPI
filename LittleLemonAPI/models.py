from rest_framework import generics
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.contrib.auth import get_user_model
CustomUser = get_user_model()


# Create your models here.


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name="customer_groups", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customer_permissions", blank=True)
    is_manager = models.BooleanField(default=False)
    is_delivery_crew = models.BooleanField(default=False)
    User = get_user_model()
    # Replace with your admin username
    admin_user = User.objects.get(username="admin")
    custom_admin_user = CustomUser.objects.get(id=admin_user.id)

    @staticmethod
    def get_users():
        return CustomUser.objects.values('id', 'username')

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
            MenuItem.objects.filter(item_of_the_day=True).update(
                item_of_the_day=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="assigned_orders")
    status = models.CharField(max_length=20, choices=[(
        'pending', 'Pending'), ('delivered', 'Delivered')])
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='cart_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart Item ID: {self.id} - {self.menu_item.title} - Qty: {self.quantity} ({self.customer.username})"

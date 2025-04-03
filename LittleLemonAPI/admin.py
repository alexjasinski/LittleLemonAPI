from django.contrib import admin
from .models import CustomUser, Category, MenuItem, Order, CartItem
# Register your models here.


class IsManagerFilter(admin.SimpleListFilter):
    title = "Manager Status"
    parameter_name = "is_manager"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Manager"),
            ("no", "Regular User"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(groups__name="Manager")
        elif self.value() == "no":
            return queryset.exclude(groups__name="Manager")


class IsDeliveryCrewFilter(admin.SimpleListFilter):
    title = "Delivery Crew Status"
    parameter_name = "is_delivery_crew"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Delivery Crew"),
            ("no", "Regular User"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(groups__name="Delivery Crew")
        elif self.value() == "no":
            return queryset.exclude(groups__name="Delivery Crew")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_manager", "is_delivery_crew")
    list_filter = ("is_manager", "is_delivery_crew")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "delivery_crew", "status", "created_at")
    list_filter = ("status", "delivery_crew")
    search_fields = ("customer__username", "status")

    def get_queryset(self, request):
        """Managers see all orders, delivery crew sees only assigned orders, customers see their own orders."""
        qs = super().get_queryset(request)

        if request.user.is_superuser or request.user.groups.filter(name="Manager").exists():
            return qs  # Managers see everything

        if request.user.groups.filter(name="Delivery Crew").exists():
            # Delivery crew sees only their assigned orders
            return qs.filter(delivery_crew=request.user)

        # Customers see only their own orders
        return qs.filter(customer=request.user)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem)

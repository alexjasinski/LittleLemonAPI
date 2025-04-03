from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django.contrib.auth import get_user_model
from .models import MenuItem, Category, Order, CartItem
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartItemSerializer
import random
import logging




# Pagination for menu items


class MenuItemPagination(PageNumberPagination):
    page_size = 5

# ViewSet for Menu Items (includes pagination & sorting)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['price']
    
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific menu item."""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

# ViewSet for Categories (added pagination & ordering)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = MenuItemPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['name']

# Order List (for admins/managers)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """If a manager/admin, return all orders. Otherwise, return only user's orders."""
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            return Order.objects.all()
        return CartItem.objects.filter(customer=CustomUser.objects.get(id=self.request.user.id))

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific order."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Managers can access all orders; users can only access their own."""
        user = self.request.user
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)


# Cart Items (Customer's cart)


logger = logging.getLogger(__name__)
CustomUser = get_user_model()


class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.info(f"User Type: {type(user)} - User: {user}")
        """Customers can only see their own cart items."""
        if not isinstance(user, CustomUser):
            raise ValueError(f"Invalid user: {user}")
        if user.is_staff:
            return CartItem.objects.all()  # Admins see all cart items
        # Customers see only their own
        return CartItem.objects.filter(customer=user)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

# Retrieve the "Item of the Day"


class ItemOfTheDayView(APIView):
    def get(self, _):
        # Fetch all menu items' IDs
        menu_items = MenuItem.objects.values_list('id', flat=True)
        if not menu_items:
            return Response({"error": "No menu items available"}, status=404)

        # Select a random ID and fetch the corresponding menu item
        random_id = random.choice(menu_items)
        item = MenuItem.objects.get(id=random_id)

        # Serialize and return the random menu item
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)

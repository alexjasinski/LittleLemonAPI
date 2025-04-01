from django.shortcuts import render
from rest_framework import generics
from .serializers import MenuItemSerializer, CategorySerializer, OrderSerializer, CartItemSerializer
from .models import MenuItem, Category, Order, CartItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response  # Import Response
# Import or define CustomUser
from django.contrib.auth.models import User as CustomUser
# Create your views here.


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class ItemOfTheDayView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.filter(item_of_the_day=True)
    serializer_class = MenuItemSerializer


class AssignOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        if not request.user.is_staff:
            return Response({"error": "Only staff members can assign orders."}, status=403)

        try:
            delivery_crew_id = request.data.get("delivery_crew_id")
            delivery_crew = CustomUser.objects.get(
                id=delivery_crew_id, is_delivery_crew=True)
            order = Order.objects.get(id=order_id, status="pending")
            order.delivery_crew = delivery_crew
            order.save()
            return Response({"message": "Order assigned successfully."}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"error": "Delivery crew not found or not valid."}, status=404)
        except Order.DoesNotExist:
            return Response({"error": "Order not found or not pending."}, status=404)


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        if not request.user.is_staff:
            return Response({"error": "Only staff members can update order status."}, status=403)

        try:
            status = request.data.get("status")
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return Response({"message": "Order status updated successfully."}, status=200)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=404)

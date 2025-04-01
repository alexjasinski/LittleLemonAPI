from django.urls import path, include
from .views import MenuItemListCreateView, CategoryListCreateView, OrderListCreateView, CartItemListCreateView, ItemOfTheDayView, AssignOrderView, UpdateOrderStatusView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list'),
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('cart-items/', CartItemListCreateView.as_view(), name='cart-item-list'),
    path('menu-items/item-of-the-day/',
         ItemOfTheDayView.as_view(), name='item-of-the-day'),
    path('orders/<int:order_id>/assign/',
         AssignOrderView.as_view(), name='assign-order'),
    path('orders/<int:order_id>/status/',
         UpdateOrderStatusView.as_view(), name='order-status'),
]

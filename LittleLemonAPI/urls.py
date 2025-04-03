from django.urls import path, include
from .views import (
    MenuItemViewSet, CategoryListCreateView, OrderListCreateView, CartItemListCreateView, CartItemDetailView,
    ItemOfTheDayView, OrderDetailView, MenuItemDetailView,
)

urlpatterns = [
    # Authentication routes using Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Category & Menu Items
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('menu-items/', MenuItemViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='menu-item-list'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(),
         name='menu-item-list-detail'),
    path('menu-items/item-of-the-day/',
         ItemOfTheDayView.as_view(), name='item-of-the-day'),

    # Orders & Cart Items
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-list-item'),
    path('cart-items/', CartItemListCreateView.as_view(), name='cart-item-list'),
    path('cart-items/<int:pk>/', CartItemDetailView.as_view(),
         name='cart-item-detail'),
]

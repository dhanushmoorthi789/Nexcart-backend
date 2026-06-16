from django.urls import path
from . import views

urlpatterns = [
    # Cart
    path('cart/', views.CartView.as_view()),
    path('cart/items/', views.CartItemView.as_view()),
    path('cart/clear/', views.CartClearView.as_view()),
    # Orders
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailView.as_view()),
    path('orders/<int:pk>/cancel/', views.CancelOrderView.as_view()),
    # Admin
    path('admin/orders/', views.AdminOrderListView.as_view()),
    path('admin/orders/<int:pk>/', views.AdminOrderDetailView.as_view()),
]

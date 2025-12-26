# backend/base/urls.py
from django.urls import path
from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    # Auth / Users
    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.registerUser, name='register'),
    path('users/profile/', views.getUserProfile, name='user-profile'),
    path('users/profile/update/', views.updateUserProfile, name='user-profile-update'),
    path('users/', views.getUsers, name='users'),
    path('users/<str:pk>/', views.getUserById, name='user-detail'),
    path('users/<str:pk>/update/', views.updateUser, name='user-update'),
    path('users/<str:pk>/delete/', views.deleteUser, name='user-delete'),

    # Products
    path('products/', views.getProducts, name='products'),
    path('products/create/', views.createProduct, name='product-create'),
    path('products/<str:pk>/', views.getProduct, name='product-detail'),
    path('products/<str:pk>/update/', views.updateProduct, name='product-update'),
    path('products/<str:pk>/delete/', views.deleteProduct, name='product-delete'),

    # Orders
    path('orders/add/', views.addOrderItems, name='orders-add'),
    path('orders/myorders/', views.getMyOrders, name='my-orders'),
    path('orders/', views.getOrders, name='all-orders'),
    path('orders/<str:pk>/', views.getOrderById, name='order-detail'),
    path('orders/<str:pk>/pay/', views.updateOrderToPaid, name='order-pay'),
]
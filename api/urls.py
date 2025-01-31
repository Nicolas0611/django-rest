from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),   
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path("orders/<uuid:order_id>/products/", views.OrderProductsAPIView.as_view(), name="order-products"),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),   
]

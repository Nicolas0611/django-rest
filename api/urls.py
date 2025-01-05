from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/info/', views.product_info),
    path('products/<int:pk>/', views.product_detail),   
    path('orders/', views.order_list),   
]

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from django.db.models import Max
from rest_framework import generics
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.views import APIView
from api.models import Product, Order,OrderItem 
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    
    "self is a reference to the current instance of the class."
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
            "It is especially useful in inheritance, where you want to extend or override behavior but still use the parent class's implementation."
        return super().get_permissions()


"This are just a class for CreateAPIView overriding the create definition"
class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):            
        print(request.data)
        return super().create(request, *args, **kwargs)

class ProductDetailAPIView(generics.RetrieveAPIView):   
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    lookup_url_kwarg = 'product_id'
    
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class=  OrderSerializer

class OrderProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        return Product.objects.filter(orders__order_id=order_id)

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class=  OrderSerializer
    permission_classes = [IsAuthenticated]

    "This view will return only the orders of the logged in user using the get_queryset method"
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'] 
        })
        return Response(serializer.data) 


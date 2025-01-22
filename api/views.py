from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from django.db.models import Max
from rest_framework import generics
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.views import APIView
from api.models import Product, Order,OrderItem 
from rest_framework.permissions import IsAuthenticated


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer


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


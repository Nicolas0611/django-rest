from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from django.shortcuts import get_object_or_404 # type: ignore
from django.db.models import Max
from rest_framework import generics
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore
from api.models import Product, Order,OrderItem 

""" @api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True) 
    return Response(serializer.data) """

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer

@api_view(['GET'])
def product_detail(request,pk):
    product= get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product) 
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('items__product')
    serializer = OrderSerializer(orders, many = True) 
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price'] 
    })
    return Response(serializer.data)

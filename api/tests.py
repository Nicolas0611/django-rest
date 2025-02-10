from django.test import TestCase
from api.models import User, Product, Order, OrderItem
from django.urls import reverse
from rest_framework import status
# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="password")
        user2 = User.objects.create_user(username="user2", password="password2")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_auth_user_orders(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)
        response = self.client.get(reverse('user-orders')) 
        orders = response.json()    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertTrue(all(order['user'] == user1.id for order in orders))
    
    def test_user_order_endpoint_retrieves_error_on_not_auth_orders(self):
        response = self.client.get(reverse('user-orders')) 
        orders = response.json()    
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(orders['detail'], "Authentication credentials were not provided.")
    
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from decimal import Decimal, InvalidOperation


class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Verify user
        user_response = requests.get(f'http://localhost:8000/api/users/{user_id}/')
        if user_response.status_code != 200:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verify product
        product_response = requests.get(f'http://localhost:8001/api/products/{product_id}/')
        if product_response.status_code != 200:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product_data = product_response.json()
        if product_data['stock'] < quantity:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        # total_price = product_data['price'] * quantity

        # Calculate total price
        product_price = Decimal(product_data['price'])
        total_price = product_price * Decimal(quantity)

        # Convert total price to Decimal
        total_price = Decimal(total_price)


        print("total price",total_price)
        # Create the order
        order = Order.objects.create(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )

        # Reduce stock
        product_data['stock'] -= quantity
        requests.put(f'http://localhost:8001/api/products/{product_id}/', data=product_data)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

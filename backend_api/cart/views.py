from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from cart.services import *


class CartView(APIView):
    def get(self, request):
        usr = request.user
        if not usr.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(user=usr)
        except ObjectDoesNotExist:
            return Response({"error": "Cart not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartItemsView(APIView):
    def get(self, request, *args, **kwargs):
        usr = request.user
        if not usr.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(user=usr)
        except ObjectDoesNotExist:
            return Response({"error": "Cart not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        usr = request.user
        cart, created_cart = Cart.objects.get_or_create(user=usr)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        try:
            cart_item = add_product_to_cart(cart, product_id, quantity)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        usr = request.user
        cart, created_cart = Cart.objects.get_or_create(user=usr)
        item_id = kwargs.get("item_id")
        quantity = request.data.get('quantity')
        cart_item, created_item = CartItem.objects.get_or_create(cart=cart, id=item_id)
        if created_item:
            return Response({"error": "No cart item found. Created new cart item with quantity 1."}, status=status.HTTP_400_BAD_REQUEST)
        if quantity is None:
            return Response({"error": "Quantity not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            update_cart_item_quantity(cart_item, quantity)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        usr = request.user
        cart_item_id = kwargs.get("cart_item_id")
        cart = Cart.objects.get(user=usr)
        try:
            delete_from_cart(cart_item_id)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartPriceView(APIView):
    def get(self, request, *args, **kwargs):
        usr = request.user
        if not usr.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        cart, created_cart = Cart.objects.get_or_create(user=usr)
        pass
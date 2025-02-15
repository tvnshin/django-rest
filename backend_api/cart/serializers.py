from rest_framework import serializers
from products.serializers import ProductSerializer
from cart.models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.total_price


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = CartSerializer()
    class Meta:
        model = CartItem
        fields = "__all__"
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def total_price(self):
        res = Decimal(0)
        cart_items = CartItem.objects.filter(cart=self)
        for item in cart_items:
            res += item.product.price_with_discount
        return res

    def __str__(self):
        return f"{self.user}'s cart"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)


    def total_price(self):
        return self.product.price * self.quantity
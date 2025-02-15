from cart.models import *
from products.models import *
from products.services import *


def update_cart_item_quantity(cart_item, quantity):
    if quantity > cart_item.quantity:
        if cart_item.product.supply > quantity - cart_item.quantity:
            take_product(cart_item.product, (quantity - cart_item.quantity))
            cart_item.quantity = quantity
            # cart_item.product.save()
            cart_item.save()
        else:
            raise Exception("Not enough product supply")
    elif quantity < cart_item.quantity:
        return_product(cart_item.product, (cart_item.quantity - quantity))
        cart_item.quantity = quantity
        cart_item.save()
    elif quantity == cart_item.quantity:
        raise Exception("Quantity is the same")


def add_product_to_cart(cart, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart_item, created_item = CartItem.objects.get_or_create(cart=cart, product=product)
    if created_item:
        update_cart_item_quantity(cart_item, quantity)
    else:
        raise Exception("Product is already in the cart")
    return cart_item


def delete_from_cart(cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if not cart_item:
        raise Exception("No such cart item with the given id")
    update_cart_item_quantity(cart_item, 0)
    cart_item.delete()


def cart_total_price(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    return sum(cart_item_price(cart_item) for cart_item in cart_items)


def cart_item_price(cart_item):
    return cart_item.product.price * cart_item.quantity


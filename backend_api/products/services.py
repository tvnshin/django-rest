from products.models import *


def return_product(product, n):
    product.supply += n
    product.save()


def take_product(product, n):
    product.supply -= n
    product.save()

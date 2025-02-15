from django.db import models
from decimal import Decimal



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class SubCategory(models.Model):
     category = models.ForeignKey(Category, default="", on_delete=models.CASCADE)
     name = models.CharField(max_length=100)

     def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(default="")
    supply = models.IntegerField(default=1)
    image = models.ImageField(upload_to="static/img/", default="static/img/insane.jpg")
    discount = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, blank=True, on_delete=models.SET_NULL, null=True)
    @property
    def price_with_discount(self):
        current_price = self.price * ((Decimal(100) - self.discount) / Decimal(100))
        current_price = current_price.quantize(Decimal('0.01'))
        return current_price
    @property
    def short_name(self):
        res = str(self.name[0]).upper()
        for i in range(1, len(self.name)):
            if self.name[i - 1] == " ":
                res += self.name[i].upper()
        formatted_id = str(self.id).zfill(2)
        res += "-" + formatted_id
        return res

    def __str__(self):
        return f"{self.name}"
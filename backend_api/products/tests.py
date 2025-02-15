from django.test import TestCase
from decimal import Decimal
from products.models import Product, Category, SubCategory


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 1")
        self.sub_category = SubCategory.objects.create(name="SubCategory 1", category=self.category)
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            discount=10,
            category=self.category,
            sub_category=self.sub_category
        )

    def test_str_representation(self):
        self.assertEqual(str(self.product), "Test Product")

    # def test_short_name(self):
    #     """Тест генерации короткого имени."""
    #     name = "TP" + str(prod)
    #     self.assertEqual(self.product.short_name, "TP-01")  # "Test Product" -> T + id=1

    def test_default_values(self):
    # default values test
        product = Product.objects.create(name="Default Product")
        self.assertEqual(product.price, Decimal(0))
        self.assertEqual(product.supply, 1)
        self.assertEqual(product.description, "")
        self.assertEqual(product.discount, Decimal(0))
        self.assertEqual(product.image, "static/img/insane.jpg")

    def test_category_relationship(self):
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.sub_category, self.sub_category)

    # def test_negative_price(self):
    #     """Тест обработки отрицательной цены."""
    #     with self.assertRaises(ValueError):
    #         Product.objects.create(name="Negative Price Product", price=-100)
    #
    def test_discount(self):
        self.assertEqual(self.product.price_with_discount, Decimal(90))

    # def test_excessive_discount(self):
    #     """Тест обработки слишком большой скидки."""
    #     product = Product(name="Excessive Discount Product", price=100, discount=110)
    #     with self.assertRaises(Exception):  # Замени Exception на ValidationError, если есть валидация
    #         product.full_clean()  # Полная проверка валидности данных
from rest_framework import serializers
from products.models import Product, SubCategory, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = SubCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    price_with_discount = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    sub_category = SubCategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"

    def get_price_with_discount(self, obj):
        return obj.price_with_discount

    def get_short_name(self, obj):
        return obj.short_name


class ProductClientSerializer(serializers.ModelSerializer):
    price_with_discount = serializers.SerializerMethodField()
    class Meta:
        model = Product
        exclude = ["supply"]

    def get_price_with_discount(self, obj):
        return obj.price_with_discount

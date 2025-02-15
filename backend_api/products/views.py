from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, SubCategory, Category
from products.serializers import ProductSerializer


class ProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleProductView(APIView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        category_name = kwargs.get('category_name')
        #sub_category_name = request.data.get('sub_category_name')
        # sub_category = SubCategory.objects.get(name=sub_category_name)
        category = Category.objects.filter(name=category_name).first()
        sub_category = SubCategory.objects.filter(name=category_name).first()
        if category:
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif sub_category:
            products = Product.objects.filter(sub_category=sub_category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

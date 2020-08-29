from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product, Seller,Category
from .serializers import ProductAllInfoSerializer, ProductSerializer, CategorySerializer,SellerSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, exceptions
from rest_framework.generics import ListAPIView
from datetime import datetime
import pytz
from django.http import Http404


class ProductList(APIView):
    """
    List all products and create new one
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductAllInfoSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_fields = (
        'category__id',
    )
    search_fields = (
        'title',
    )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class SellerViewSet(viewsets.ModelViewSet):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()

class ReportView(APIView):
    def post(self, request):
        data = request.data
        self.validatedata(data)
        category = data.get('category')
        products = data.get('products')
        date = data.get('date')
        category_obj = self.get_category(category)
        response = self.handle_products(category_obj, products, date)
        return Response({"message": response})

    def handle_products(self, category_obj, products, date):
        response = []
        for product in products:
            seller_obj, _ = Seller.objects.get_or_create(name=product.get('seller'))
            date_formatted = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
            date_formatted = pytz.utc.localize(date_formatted)
            obj, created = Product.objects.update_or_create(
                asin=product.get('asin'),
                seller=seller_obj,
                category=category_obj,
                defaults={
                    'photo': product.get('photo'),
                    'updated': date_formatted,
                    'price': product.get('price'),
                    'title': product.get('title'),
                }
            )
            if created:
                response.append(f'{obj.asin} - {obj.title} - created')
            else:
                response.append(f'{obj.asin} - {obj.title} - updated')
                print(response)
        return response

    def validatedata(self, data):
        if data.get('category') is None:
            raise exceptions.ValidationError(
                'category is null'
            )
        if data.get('products') is None:
            raise exceptions.ValidationError(
                'products is null'
            )
        if data.get('date') is None:
            raise exceptions.ValidationError(
                'date is null'
            )
    def get_category(self, category):
        obj, _ = Category.objects.get_or_create(name=category.title)
        return obj

class ProductDetail(APIView):
    """
    Retrieve, delete a product instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
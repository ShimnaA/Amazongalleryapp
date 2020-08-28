from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product, Seller,Category
from .serializers import ProductAllInfoSerializer, ProductSerializer, CategorySerializer,SellerSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
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

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class SellerViewSet(viewsets.ModelViewSet):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
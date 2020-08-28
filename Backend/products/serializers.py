from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, Seller, Category

class CategorySerializer(ModelSerializer):
    random_photo = SerializerMethodField()

    def get_random_photo(self, obj):
        try:
            obj.products.first().photo
        except:
            return ""

    class Meta:
        model = Category
        fields= (
            'id',
            'name',
            'random_photo'
        )

class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            'id',
            'name'
        )

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'photo',
            'price',
            'title',
            'category',
            'seller',
        )

class ProductAllInfoSerializer(ModelSerializer):
    category = CategorySerializer()
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'photo',
            'price',
            'title',
            'category',
            'seller'
        )
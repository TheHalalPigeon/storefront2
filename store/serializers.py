from rest_framework import serializers

from decimal import Decimal

from .models import Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id", 
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price", 
            "price_with_tax", 
            "collection"
        ]
        # fields = ["__all__"] <-- BAD
    
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance: Product, validated_data):
    #     instance.unit_price = validated_data.get("unit_price")
    #     instance.save()
    #     return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)
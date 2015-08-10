from rest_framework import serializers
from .models import SubscriptionPlan, State, City, User, Company, PushNotification, Sale, SaleResponse, ProductImage, \
    Category, IndustryVertical, Brand


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'state')


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ('id', 'name', 'description', 'duration')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'mobile_no', 'first_name', 'last_name', 'company', 'date_joined')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = ('id', 'gcm_id', 'imei_no', 'phone_no', 'mobile_make', 'mobile_model', 'os_version', 'app_version')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product', 'image', 'order', 'id')


class SaleSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    company = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Sale
        fields = ('id',
                  'company',
                  'category',
                  'brand',
                  'model',
                  'description',
                  'min_quantity',
                  'unit_of_measure',
                  'price_in_inr',
                  'new',
                  'refurbished',
                  'warranty',
                  'start_date',
                  'end_date',
                  'shipped_to',
                  'box_contents',
                  'active',
                  'created_by',
                  'images',
                  )

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        shipped_to = validated_data.pop('shipped_to')
        product = Sale.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        product.shipped_to = shipped_to
        product.save()

        return product




class SaleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleResponse


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class IndustryVerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryVertical


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand

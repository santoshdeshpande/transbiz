from rest_framework import serializers

from .models import *


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
        fields = ('id', 'product', 'image', 'order')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand


class IndustryVerticalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryVertical


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question')


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
                  'saleItem',
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


class IndustryVerticalCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = IndustryVertical


class SignUpSerializer(serializers.Serializer):
    username = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(max_length=70)
    last_name = serializers.CharField(max_length=70)
    mobile_no = serializers.CharField(max_length=13)

    company_name = serializers.CharField(max_length=200)
    address_line_1 = serializers.CharField(max_length=200)
    address_line_2 = serializers.CharField(max_length=200, allow_blank=True)
    city = serializers.StringRelatedField()
    state = serializers.StringRelatedField()
    pin_code = serializers.CharField(max_length=20)
    landline_number = serializers.CharField(max_length=20)
    tin = serializers.CharField(max_length=11)
    tan = serializers.CharField(max_length=10)
    service_tax_number = serializers.CharField(max_length=15)
    ie_number = serializers.CharField(max_length=10)
    website = serializers.URLField(allow_blank=True)
    established_year = serializers.IntegerField()
    logo = serializers.ImageField(allow_empty_file=True)

    fields = ('username', 'password', 'first_name', 'last_name', 'mobile_no', 'company_name', 'address_line_1',
              'address_line_2', 'city', 'state', 'pin_code', 'landline_number', 'tin', 'tan',
              'service_tax_number', 'ie_number', 'website', 'established_year', 'logo')

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        mobile_no = validated_data.pop('mobile_no')

        company_name = validated_data.pop('company_name')
        address_line_1 = validated_data.pop('address_line_1')
        address_line_2 = validated_data.pop('address_line_2')
        city = City.objects.all().filter(pk=validated_data.pop('city'))
        state = State.objects.all().filter(pk=validated_data.pop('state'))
        pin_code = validated_data.pop('pin_code')
        landline_number = validated_data.pop('landline_number')
        tin = validated_data.pop('tin')
        tan = validated_data.pop('tan')
        service_tax_number = validated_data.pop('service_tax_number')
        ie_number = validated_data.pop('ie_number')
        website = validated_data.pop('website')
        established_year = validated_data.pop('established_year')
        logo = validated_data.pop('logo')

        company = Company.objects.create(name=company_name, address_line_1=address_line_1,
                                         address_line_2=address_line_2, city=city, state=state, pin_code=pin_code,
                                         landline_number=landline_number, tin=tin, tan=tan,
                                         service_tax_number=service_tax_number,
                                         ie_number=ie_number, website=website, active=False,
                                         established_year=established_year,
                                         logo=logo, verified=False)

        user = User.objects.create(first_name=first_name, last_name=last_name, mobile_no=mobile_no,
                                   company=company, password=password)


class BuyRequestSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    shipped_to_full = CitySerializer(many=True, source='shipped_to', read_only=True, required=False)

    class Meta:
        model = BuyRequest
        fields = ('id',
                  'is_closed',
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
                  'delivery_date',
                  'shipped_to_full',
                  'shipped_to',
                  'created_by',
                  'saleItem'
                  )

    def create(self, validated_data):
        print validated_data
        # print validated_data.pop('delivery_date')
        user = validated_data['created_by']
        validated_data['company'] = user.company
        shipped_to = validated_data.pop('shipped_to')
        buy_request = BuyRequest.objects.create(**validated_data)
        buy_request.company_id = user.company.id
        buy_request.shipped_to = shipped_to
        buy_request.save()
        return buy_request


class BuyResponseSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    shipped_to_full = CitySerializer(many=True, source='shipped_to', required=False, read_only=True)
    # shipped_to_id = serializers.PrimaryKeyRelatedField(required=False, many=True, source='shipped_to', read_only=True)

    class Meta:
        model = BuyResponse
        fields = ('id',
                  'buy_request',
                  'is_deal',
                  'created_by',
                  'comments',
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
                  'delivery_date',
                  'shipped_to',
                  'shipped_to_full',
                  'saleItem',
                  'box_contents'
                  )

    def validate(self, data):
        print data
        return data

    def create(self, validated_data):
        print validated_data
        # print validated_data.pop('delivery_date')
        user = validated_data['created_by']
        validated_data['company'] = user.company
        shipped_to = validated_data.pop('shipped_to')
        buy_request = BuyResponse.objects.create(**validated_data)
        buy_request.company_id = user.company.id
        buy_request.shipped_to = shipped_to
        buy_request.save()
        return buy_request

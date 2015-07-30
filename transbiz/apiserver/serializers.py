from rest_framework import serializers
from .models import SubscriptionPlan, State, City, User, Company, PushNotification, Sale


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

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        #fields = ('id','company','category','brand','model','description','min_quantity','unit_of_measure','price_in_inr','new','refurbished','warranty','start_date')

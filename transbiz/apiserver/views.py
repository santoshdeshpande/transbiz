import re

from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .serializers import *
from .models import Question, ProductImage, BuyRequest
from .serializers import StateSerializer, CitySerializer, UserSerializer, CompanySerializer, \
    PushNotificationSerializer, SaleSerializer, SaleResponseSerializer, CategorySerializer, \
    IndustryVerticalSerializer, IndustryVerticalCategorySerializer, BrandSerializer, SignUpSerializer
from .models import State, City, User, Company, PushNotification, Sale, SaleResponse, Category, IndustryVertical, Brand


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StateViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.company == settings.TRANSBIZ_COMPANY_NAME:
            return self.queryset
        return Company.objects.filter(pk=user.company.id)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(company=user.company)

    @list_route()
    def profile(self, request):
        current_user = User.objects.get(pk=request.user.id)
        serializer = self.get_serializer(current_user)
        return Response(serializer.data)


class PushNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = PushNotificationSerializer
    queryset = PushNotification.objects.all()

    def get_queryset(self):
        user = self.request.user
        return PushNotification.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        sales_queryset = Sale.objects.exclude(end_date__lt=timezone.now()).filter(active=True)
        category_id = self.request.query_params.get('category_id', None)
        is_new = self.request.query_params.get('new', None)
        is_old = self.request.query_params.get('old', None)
        sort = self.request.query_params.get('sort', None)
        if category_id is not None:
            sales_queryset = sales_queryset.filter(category_id=category_id)
        if is_new is not None:
            sales_queryset = sales_queryset.filter(new=(is_new == str('true')))
        if is_old is not None:
            sales_queryset = sales_queryset.filter(refurbished=(is_old == str('true')))
        if sort is not None:
            sales_queryset = sales_queryset.order_by(sort)

        return sales_queryset

    def perform_create(self, serializer):
        images = self.get_images_dict()
        serializer.save(company=self.request.user.company, images=images)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user.company)

    def get_images_dict(self):
        files = self.request.FILES
        images = []
        for key in files:
            search = re.search(r'images_(\d+)_', key)
            if search:
                image = {'image': files[key]}
                file_index = search.groups()[0]
                order_key = 'images_%s_order' % str(file_index)
                if order_key in self.request.DATA:
                    image['order'] = self.request.DATA[order_key]
                images.append(image)
        return images


class SaleResponseViewSet(viewsets.ModelViewSet):
    serializer_class = SaleResponseSerializer
    queryset = SaleResponse.objects.all()


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = IndustryVerticalCategorySerializer
    queryset = IndustryVertical.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class IndustryVerticalViewSet(viewsets.ModelViewSet):
    serializer_class = IndustryVerticalSerializer
    queryset = IndustryVertical.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class SignUpViewSet(viewsets.ViewSet):
    serializer_class = SignUpSerializer


class MyTradesViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()

    def get_queryset(self):
        user = self.request.user.id
        return Sale.objects.filter(created_by=user).exclude(end_date__lt=timezone.now()).filter(active=True)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class BuyRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BuyRequestSerializer
    queryset = BuyRequest.objects.all()


class BuyResponseViewSet(viewsets.ModelViewSet):
    serializer_class = BuyResponseSerializer
    queryset = BuyResponse.objects.all()

    def get_queryset(self):
        buy_request = self.request.query_params.get('buy_request')
        queryset = BuyResponse.objects.all()
        if buy_request:
            queryset = queryset.filter(buy_request=buy_request)
        return queryset


class UserRegistration(APIView):
    def post(self, request, format=None):
        user_data = request.data["user"]
        company_data = request.data["company"]
        connection_data = request.data["connections"]

        company_serializer = CompanySerializer(data=company_data)
        is_valid_company = company_serializer.is_valid()
        if not is_valid_company:
            return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        company = company_serializer.save()

        user_data["company_id"] = company.id
        user_serializer = UserSerializer(data=user_data)
        is_valid_user = user_serializer.is_valid()
        if not is_valid_user:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.create(user_data)
        return Response(status=status.HTTP_201_CREATED)

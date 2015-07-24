from rest_framework.decorators import list_route
from .serializers import StateSerializer, CitySerializer, UserSerializer, CompanySerializer
from rest_framework import viewsets
from .models import State, City, User, Company
from rest_framework.response import Response
from django.conf import settings

class StateViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

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

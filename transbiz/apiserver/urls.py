from rest_framework.routers import DefaultRouter
from .views import StateViewSet, CityViewSet, UserViewSet, CompanyViewSet, PushNotificationViewSet, SaleViewSet

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

# place app url patterns here
router = DefaultRouter()
router.register('states', StateViewSet)
router.register('cities', CityViewSet)
router.register('users', UserViewSet)
router.register('companies', CompanyViewSet)
router.register('notifications', PushNotificationViewSet)
router.register('sales', SaleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),

]

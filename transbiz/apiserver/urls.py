from rest_framework.routers import DefaultRouter

from .views import *

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
router.register('saleresponse', SaleResponseViewSet)
router.register('product_image', ProductImageViewSet)
router.register('categories', CategoryViewSet)
router.register('dashboard', DashboardViewSet)
router.register('verticals', IndustryVerticalViewSet)
router.register('brands', BrandViewSet)
router.register('questions', QuestionViewSet)
router.register('myTrades', MyTradesViewSet)
router.register('buyRequest', BuyRequestViewSet)
router.register('buyResponse', BuyResponseViewSet)
# router.register('sign-up', UserRegistration)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^sign-up/', UserRegistration.as_view(), name="SignUp")
]

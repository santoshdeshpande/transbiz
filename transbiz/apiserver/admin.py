from django.contrib import admin
from .models import State, IndustryVertical, Category, SubscriptionPlan, City, Subscription, Company

admin.site.register(State)
admin.site.register(IndustryVertical)
admin.site.register(Category)
admin.site.register(SubscriptionPlan)
admin.site.register(City)
admin.site.register(Company)
admin.site.register(Subscription)

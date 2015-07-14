from django.contrib import admin
from transbiz.apiserver.models import State, IndustryVertical, Category, SubscriptionPlan, City

admin.site.register(State)
admin.site.register(IndustryVertical)
admin.site.register(Category)
admin.site.register(SubscriptionPlan)
admin.site.register(City)

from django.contrib import admin
from .models import State, IndustryVertical, Category, SubscriptionPlan, City, Subscription, Company, User, Brand, \
    Sale, PushNotification, ProductImage, SaleResponse, Question, BuyRequest, BuyResponse
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", 'mobile_no')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("An user with the email %s already exists" % email);

    def clean_mobile_no(self):
        mobile = self.cleaned_data["mobile_no"]
        try:
            User.objects.get(mobile_no=mobile)
        except User.DoesNotExist:
            return mobile
        raise forms.ValidationError("An user with the phone %s already exists" % mobile);

from django.contrib.postgres.fields import ArrayField
admin.site.register(State)
admin.site.register(IndustryVertical)
admin.site.register(Category)
admin.site.register(SubscriptionPlan)
admin.site.register(City)
admin.site.register(Company)
admin.site.register(Subscription)
admin.site.register(Brand)
#admin.site.register(Sale)
admin.site.register(PushNotification)
#admin.site.register(ProductImage)
admin.site.register(SaleResponse)
admin.site.register(Question)
admin.site.register(BuyRequest)
admin.site.register(BuyResponse)

@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('mobile_no', 'email', 'company','first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('mobile_no', 'first_name', 'last_name', 'email')
    ordering = ('mobile_no','email')

    fieldsets = (
        (None, {'fields': ('email', 'mobile_no', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'company')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','mobile_no','company', 'password1', 'password2'),
        }),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines=[
    ProductImageInline,
    ]

# admin.site.register(User, UserAdmin)

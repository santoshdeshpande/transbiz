from datetime import date

from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.db import models, IntegrityError

from django.core.exceptions import ValidationError
from django.db import models
from datetime import date, timedelta
# Create your models here.
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4


class State(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True, verbose_name='Name of the State', blank=False)
    short_name = models.CharField(max_length=2, verbose_name='Short Name for the State(KA, MH etc)', blank=False)

    def __unicode__(self):
        return self.name


class City(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True, verbose_name='Name of the city')
    state = models.ForeignKey(State, related_name='cities')

    class Meta:
        verbose_name_plural = 'Cities'
        verbose_name = 'City'

    def __unicode__(self):
        return self.name


class IndustryVertical(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    logo_image = models.ImageField(blank=True, null=True, upload_to='vertical_logo', verbose_name="Verical Logo")

    class Meta:
        verbose_name_plural = 'Industry Verticals'
        verbose_name = 'Industry Vertical'

    def __unicode__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    vertical = models.ForeignKey(IndustryVertical, related_name="categories")

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class SubscriptionPlan(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, verbose_name='Number of days for this plan')

    class Meta:
        verbose_name_plural = "Subscription Plans"
        verbose_name = "Subscription Plan"

    def __unicode__(self):
        return "%s (%d days) " % (self.name, self.duration)


class Company(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.ForeignKey(City)
    state = models.ForeignKey(State)
    pin_code = models.CharField(max_length=20)
    landline_number = models.CharField(max_length=20)
    tin = models.CharField(max_length=11, verbose_name='Tax-Payer Identification Number')
    tan = models.CharField(max_length=10, verbose_name='Tax Deduction and Collection Account Number (TAN)')
    service_tax_number = models.CharField(max_length=15)
    ie_number = models.CharField(max_length=10, verbose_name='Import Export Code Number', blank=True)
    website = models.URLField(blank=True)
    active = models.BooleanField(default=False)
    established_year = models.PositiveIntegerField(validators=[MinValueValidator(1950)], blank=True, null=True)
    verified = models.BooleanField(default=False)
    logo = models.ImageField(blank=True, null=True, upload_to='logos')

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.state = self.city.state
        super(Company, self).save(force_insert, force_update, using, update_fields)

    @property
    def has_valid_subscriptions(self):
        for subscription in self.subscriptions.all():
            if subscription.is_active:
                return True
        return False

    @property
    def is_active(self):
        return self.active and self.verified

    def __unicode__(self):
        return self.name


class Brand(TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name="Name of the model")
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = "Brands"
        verbose_name = "Brand"
        unique_together = ('name', 'category')

    def __unicode__(self):
        return self.name


class SubscriptionManager(models.Manager):
    def has_overlapped_subscriptions(self, start_date, end_date, vertical):
        overlapped_on_start = self.get_queryset().filter(vertical__id=vertical.id,
                                                         start_date__range=[start_date, end_date]).count()
        overlapped_on_end = self.get_queryset().filter(vertical_id=vertical.id,
                                                       end_date__range=[start_date, end_date]).count()
        return (overlapped_on_start + overlapped_on_end) > 0


class Subscription(TimeStampedModel):
    plan = models.ForeignKey(SubscriptionPlan)
    company = models.ForeignKey(Company, related_name='subscriptions')
    vertical = models.ForeignKey(IndustryVertical, default=None)
    start_date = models.DateField()
    end_date = models.DateField()

    objects = SubscriptionManager()

    def __unicode__(self):
        return "%s - %s" % (self.company, self.plan)

    @property
    def is_active(self):
        return self.end_date >= date.today() >= self.start_date

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # print self.instance
        if Subscription.objects.has_overlapped_subscriptions(self.start_date, self.end_date, self.vertical):
            raise ValidationError("There are overlapping subscriptions")
        super(Subscription, self).save(force_insert, force_update, using, update_fields)
        return date.today() <= self.end_date


def get_end_date():
    return timezone.now() + timedelta(days=settings.DEFAULT_SALE_TIME)

UOM = (
        ('pcs', 'Pieces'),
        ('pcks', 'Packs'),)

class Sale(TimeStampedModel):

    company = models.ForeignKey(Company)
    category = models.ForeignKey(Category, related_name='sales')
    brand = models.ForeignKey(Brand)
    model = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    min_quantity = models.PositiveIntegerField(verbose_name="Minimum quantity", validators=[MinValueValidator(1)])
    unit_of_measure = models.CharField(max_length=10, choices=UOM)
    price_in_inr = models.PositiveIntegerField(default=0)
    new = models.BooleanField(default=True)
    refurbished = models.BooleanField(default=True)
    warranty = models.PositiveIntegerField(verbose_name="Warranty in number of months", default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=get_end_date)
    shipped_to = models.ManyToManyField(City)
    box_contents = models.CharField(max_length=200, blank="True")
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def _sale_item(self):
        return '%s %s %s' %(self.category.name, self.brand.name, self.model)
        # return self.category.name +" "+ self.brand.name +" "+ self.model

    saleItem = property(_sale_item) 

    class Meta:
        verbose_name_plural = "Sales"
        verbose_name = "Sale"

    def clean(self):
        super(Sale, self).clean()
        if self.start_date < timezone.now():
            raise ValidationError('Start date cannot be in the past')

    def __unicode__(self):
        return "%s/%s/%s" % (self.brand, self.category, self.model)

    @property
    def is_active(self):
        date_now = date.today()
        return self.active and (date_now >= self.start_date.date()) and (date_now <= self.end_date.date())

    
    

class PushNotification(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    gcm_id = models.CharField(max_length=400)
    imei_no = models.CharField(max_length=16)
    phone_no = models.CharField(max_length=10, blank=True)
    mobile_make = models.CharField(max_length=50)
    mobile_model = models.CharField(max_length=50)
    os_version = models.CharField(max_length=50)
    app_version = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Push Notifications"
        verbose_name = "Push Notification"

    def __unicode__(self):
        return unicode(self.user)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return filename


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Sale, related_name="images")
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Product Images"
        verbose_name = "ProductImage"

    def __unicode__(self):
        return "%s - %s" % (self.product, self.order)

    def clean(self):
        if not self.validate_number_of_images_per_sale():
            raise ValidationError("Limit on number of images for %s has been reached" % self.product)

    def validate_number_of_images_per_sale(self):
        count = ProductImage.objects.filter(product=self.product).count()
        if count >= 3:
            return False
        return True


class Question(TimeStampedModel):
    question = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Questions"
        verbose_name = "Question"

    def __unicode__(self):
        return unicode(self.question)


class SaleResponse(TimeStampedModel):
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Sale)
    questions = models.ManyToManyField(Question)
    cities = models.ManyToManyField(City)
    qty_wanted = models.PositiveIntegerField(verbose_name="Quantity Wanted", validators=[MinValueValidator(1)])
    comments = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Sale Responses"
        verbose_name = "Sale Response"

    def __unicode__(self):
        return unicode(self.product)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, mobile_no, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, mobile_no=mobile_no,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, mobile_no=None, password=None, **extra_fields):
        return self._create_user(email, mobile_no, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, mobile_no, password, **extra_fields):
        company = Company.objects.get(name__exact=settings.TRANSBIZ_COMPANY_NAME)
        return self._create_user(email, mobile_no, password, True, True, company=company,
                                 **extra_fields)

    def can_create_more_users(self, company):
        if company.name == settings.TRANSBIZ_COMPANY_NAME:
            return True
        all_users = self.get_queryset().filter(company__id=company.id).count()
        return all_users <= settings.DEFAULT_USER_CREATION_COUNT


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email Address', unique=True, error_messages={
        'unique': _("A user with that email address already exists."),
    })
    mobile_no = models.CharField(max_length=13)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    company = models.ForeignKey(Company, blank=True, related_name='users', null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no']

    objects = UserManager()

    def clean(self):
        if not User.objects.can_create_more_users(self.company):
            raise ValidationError("The maximum number of users for this company has reached")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not User.objects.can_create_more_users(self.company):
            raise ValidationError("The maximum number of users for this company has reached")
        super(User, self).save(force_insert, force_update, using, update_fields)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def _belongs_to_optibiz(self):
        return self.company.name == settings.TRANSBIZ_COMPANY_NAME

    def is_valid_login(self):
        if self._belongs_to_optibiz():
            return True
        return self.company.is_active and self.company.has_valid_subscriptions


class BuyRequest(TimeStampedModel):
    company = models.ForeignKey(Company)
    category = models.ForeignKey(Category, related_name='buy_request')
    brand = models.ForeignKey(Brand, null=True, blank=True)
    model = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    min_quantity = models.PositiveIntegerField(verbose_name="Minimum quantity", validators=[MinValueValidator(1)])
    unit_of_measure = models.CharField(max_length=10, choices=UOM)
    price_in_inr = models.PositiveIntegerField(default=0)
    new = models.BooleanField(default=True)
    refurbished = models.BooleanField(default=True)
    warranty = models.PositiveIntegerField(verbose_name="Warranty in number of months", default=0)
    delivery_date = models.DateTimeField(default=timezone.now)
    shipped_to = models.ManyToManyField(City)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def _sale_item(self):
        return '%s %s %s' %(self.category.name, self.brand.name, self.model)

    saleItem = property(_sale_item)


class BuyResponse(TimeStampedModel):
    buy_request = models.ForeignKey(BuyRequest,related_name='buy_request')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    comments = models.CharField(max_length=200, blank=True)
    company = models.ForeignKey(Company)
    category = models.ForeignKey(Category, related_name='buy_response')
    brand = models.ForeignKey(Brand, null=True, blank=True)
    model = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    min_quantity = models.PositiveIntegerField(verbose_name="Minimum quantity", validators=[MinValueValidator(1)])
    unit_of_measure = models.CharField(max_length=10, choices=UOM)
    price_in_inr = models.PositiveIntegerField(default=0)
    new = models.BooleanField(default=True)
    refurbished = models.BooleanField(default=True)
    warranty = models.PositiveIntegerField(verbose_name="Warranty in number of months", default=0)
    delivery_date = models.DateTimeField(default=timezone.now)
    shipped_to = models.ManyToManyField(City)
    box_contents = models.CharField(max_length=200, blank="True")

    def _sale_item(self):
        return '%s %s %s' %(self.category.name, self.brand.name, self.model)

    saleItem = property(_sale_item)

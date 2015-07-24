from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.db import models
from datetime import date
# Create your models here.
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import six, timezone
from django.utils.translation import ugettext, ugettext_lazy as _


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

    class Meta:
        verbose_name_plural = 'Industry Verticals'
        verbose_name = 'Industry Vertical'

    def __unicode__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    vertical = models.ForeignKey(IndustryVertical)

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

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.state = self.city.state
        super(Company, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.name


class Subscription(TimeStampedModel):
    plan = models.ForeignKey(SubscriptionPlan)
    company = models.ForeignKey(Company)
    vertical = models.ForeignKey(IndustryVertical, default=None)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return "%s - %s" % (self.company, self.plan)

    @property
    def is_active(self):
        return date.today() <= self.end_date


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
        company = Company.objects.get(name__exact='Optibiz')
        return self._create_user(email, mobile_no, password, True, True, company=company,
                                 **extra_fields)


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(User, self).save(force_insert, force_update, using, update_fields)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

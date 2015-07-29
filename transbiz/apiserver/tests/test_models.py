import unittest
import datetime
from django.db import IntegrityError
from ..models import City, State, IndustryVertical, Category, SubscriptionPlan, Company, Subscription, Brand, Sale, PushNotification, User
from config.settings.common import DEFAULT_SALE_TIME

class TestCityModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_city_does_not_allow_duplicate_names(self):
        self.state = State.objects.create(name='Karnatak', short_name='KA')
        city = City.objects.create(name='Bangaloe', state=self.state)
        self.assertIsNotNone(city, "A city object should have been created")
        city = City(name='Bangalore', state=self.state)
        with self.assertRaises(IntegrityError):
            city.save()

    def test_city_does_not_allow_state_to_be_empty(self):
        city = City(name='Delhi')
        with self.assertRaises(IntegrityError):
            city.save()


class TestStateModel(unittest.TestCase):
    def test_state_does_not_allow_empty_name(self):
        with self.assertRaises(IntegrityError):
            state = State(short_name='XX', name=None)
            state.save()

    def test_state_does_not_allow_empty_short_name(self):
        with self.assertRaises(IntegrityError):
            State.objects.create(name='XXXX', short_name=None)


class TestIndustryVerticalModel(unittest.TestCase):
    def test_name_is_mandatory(self):
        with self.assertRaises(IntegrityError):
            IndustryVertical.objects.create(active=False, description='XXXX', name=None)

    def test_default_create_has_active_True(self):
        vertical, result = IndustryVertical.objects.get_or_create(name='Infotech')
        self.assertEqual(vertical.active, True)
        self.assertEqual(vertical.description, None)
        self.assertEqual(vertical.name, 'Infotech')

    def test_duplicate_names_are_not_allowed(self):
        with self.assertRaises(IntegrityError):
            IndustryVertical.objects.create(name='Infotech')
            IndustryVertical.objects.create(name='Infotech')


class TestCategoryModel(unittest.TestCase):
    def test_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            vertical, result = IndustryVertical.objects.get_or_create(name='Infotech')
            Category.objects.create(name='Laptops', vertical=vertical)
            Category.objects.create(name='Laptops', vertical=vertical)

    def test_a_valid_category(self):
        vertical, result = IndustryVertical.objects.get_or_create(name='Infotech')
        obj = Category.objects.create(name='Mouse', vertical=vertical, description='Some text')
        actual = Category.objects.get(id=obj.id)
        self.assertIsNotNone(actual)
        self.assertEqual(actual.name, 'Mouse')
        self.assertEqual(actual.vertical.id, vertical.id)
        self.assertEqual(actual.description, obj.description)


class TestSubscriptionPlan(unittest.TestCase):
    def test_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            SubscriptionPlan.objects.create(name='sumeru')
            SubscriptionPlan.objects.create(name='sumeru')

    def test_duration_is_zero_by_default(self):
        obj = SubscriptionPlan.objects.create(name='parvata')
        self.assertEqual(obj.duration, 0)
        self.assertEqual(obj.description, None)


class TestCompanyModel(unittest.TestCase):
    def setUp(self):
        self.state, result = State.objects.get_or_create(name='Karnataka', short_name='KA')
        self.city, result = City.objects.get_or_create(name='Bangalore', state=self.state)
        self.default_company = Company(name='Apple', address_line_1='Somewhere', city=self.city, state=self.state,
                                       pin_code='560010', landline_number='080-35353534', tin='1111111',
                                       tan='111111111', service_tax_number='11111111', )

    def test_a_valid_company_is_saved(self):
        self.default_company.save()
        self.assertEqual(self.default_company.name, 'Apple')

    def test_company_name_should_be_unique(self):
        with self.assertRaises(IntegrityError):
            self.default_company.save()
            company_another = Company(name='Apple', address_line_1='Somewhere', city=self.city, state=self.state,
                                      pin_code='560010', landline_number='080-35353534', tin='1111111', tan='111111111',
                                      service_tax_number='11111111', )
            company_another.save()

    def test_not_valid_if_address_1_is_missing(self):
        with self.assertRaises(IntegrityError):
            self.default_company.address_line_1 = None
            self.default_company.save()

    def test_not_valid_if_city_state_are_missing(self):
        with self.assertRaises(ValueError):
            company_another = Company(name='Apple1', address_line_1='Somewhere', city=None, state=None,
                                      pin_code='560010', landline_number='080-35353534', tin='1111111', tan='111111111',
                                      service_tax_number='11111111', )
            company_another.save()

    def test_state_is_set_based_on_the_city_chosen(self):
        another_state, result = State.objects.get_or_create(name='Maharashtra', short_name='MH')
        company_another = Company(name='Apple2', address_line_1='Somewhere', city=self.city, state=another_state,
                                  pin_code='560010', landline_number='080-35353534', tin='1111111', tan='111111111',
                                  service_tax_number='11111111', )
        company_another.save()
        self.assertEqual(company_another.state.short_name, 'KA')


class TestSubscriptionPlan(unittest.TestCase):
    def setUp(self):
        self.vertical,result = IndustryVertical.objects.get_or_create(name="Infotech")
        self.state, result = State.objects.get_or_create(name='Karnataka', short_name='KA')
        self.city, result = City.objects.get_or_create(name='Bangalore', state=self.state)
        self.company, result = Company.objects.get_or_create(name='AppleSub', address_line_1='Somewhere',
                                                             city=self.city, state=self.state,
                                                             pin_code='560010', landline_number='080-35353534',
                                                             tin='1111111',
                                                             tan='111111111', service_tax_number='11111111', )
        self.plan, result = SubscriptionPlan.objects.get_or_create(name='sumeru')

    def test_a_valid_subscription(self):
        subscription = Subscription.objects.create(plan=self.plan, company=self.company,
                                                   vertical=self.vertical,
                                                   start_date=datetime.date(2010, 1, 20),
                                                   end_date=datetime.date(2020, 1, 20))
        self.assertIsNotNone(subscription.id)
        self.assertTrue(subscription.is_active)


class TestBrandModel(unittest.TestCase):

    def setUp(self):
        self.vertical, result = IndustryVertical.objects.get_or_create(name='Infotech')
        self.category, result = Category.objects.get_or_create(name="Laptop",vertical=self.vertical)
        self.brand, result = Brand.objects.get_or_create(name="Acer", category = self.category)

    def test_a_valid_brand(self):
        self.assertEqual(self.brand.name, 'Acer')
        self.assertEqual(self.brand.category,self.category)

    def test_name_category_pair_must_be_unique(self):
        category_another = Category.objects.create(name="Harddisk",vertical=self.vertical)
        brand2 = Brand.objects.create(name="Acer", category = category_another)
        self.assertIsNotNone(self.brand)
        self.assertIsNotNone(brand2)

    def test_name_is_unique_for_a_category(self):
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="Acer", category = self.category)

class TestSaleModel(unittest.TestCase):

    def setUp(self):
        self.state, result = State.objects.get_or_create(name='Karnataka', short_name='KA')
        self.city, result = City.objects.get_or_create(name='Bangalore', state=self.state)
        self.vertical, result = IndustryVertical.objects.get_or_create(name='Infotech')
        self.category, result = Category.objects.get_or_create(name="Laptop",vertical=self.vertical)
        self.company, result = Company.objects.get_or_create(name='AppleSub', address_line_1='Somewhere',
                                                             city=self.city, state=self.state,
                                                             pin_code='560010', landline_number='080-35353534',
                                                             tin='1111111',
                                                             tan='111111111', service_tax_number='11111111')
        self.brand, result = Brand.objects.get_or_create(name="iOS", category = self.category)
        self.start_date = datetime.datetime.now()
        self.end_date = datetime.datetime.now() + datetime.timedelta(days = 7)
        self.sale = Sale(company= self.company, category = self.category,
                         brand = self.brand, model = "proair", min_quantity = 2,
                         unit_of_measure = "pcs",price_in_inr = 24000,
                         new = True, refurbished = True, warranty = 24,
                         start_date=self.start_date, 
                         end_date = self.end_date,
                         active = False )


    def test_a_valid_sale(self):
        self.assertEqual(self.sale.company, self.company)
        self.assertEqual(self.sale.category, self.category)
        self.assertEqual(self.sale.brand, self.brand)
        self.assertEqual(self.sale.model, "proair")
        self.assertEqual(self.sale.min_quantity, 2)
        self.assertEqual(self.sale.unit_of_measure, "pcs")
        self.assertEqual(self.sale.price_in_inr, 24000)
        self.assertTrue(self.sale.new)
        self.assertTrue(self.sale.refurbished)
        self.assertEqual(self.sale.warranty, 24)
        self.assertEqual(self.sale.start_date, self.start_date)
        self.assertEqual(self.sale.end_date, self.end_date)
        self.assertFalse(self.sale.active)
        self.assertFalse(self.sale.is_active)

    def test_not_valid_if_min_quantity_is_negative(self):
        with self.assertRaises(IntegrityError):
            self.sale.min_quantity = -4
            self.sale.save()

    def test_not_valid_if_company_is_missing(self):
        with self.assertRaises(IntegrityError):
            another_sale = Sale(category = self.category,
                                brand = self.brand, model = "proair", min_quantity = 2,
                                unit_of_measure = "pcs",price_in_inr = 24000,
                                new = True, refurbished = True, warranty = 24,
                                start_date= self.start_date, 
                                end_date = self.end_date,
                                active = False )
            another_sale.save()

    def test_not_valid_if_category_is_missing(self):
        with self.assertRaises(IntegrityError):
            another_sale = Sale(company = self.company,
                                brand = self.brand, model = "proair", min_quantity = 2,
                                unit_of_measure = "pcs",price_in_inr = 24000,
                                new = True, refurbished = True, warranty = 24,
                                start_date= self.start_date, 
                                end_date = self.end_date,
                                active = False )
            another_sale.save()

    def test_not_valid_if_model_is_missing(self):
        with self.assertRaises(IntegrityError):
            another_sale = Sale(category = self.category,company = self.company,
                                brand = self.brand, min_quantity = 2,
                                model = None,
                                unit_of_measure = "pcs",price_in_inr = 24000,
                                new = True, refurbished = True, warranty = 24,
                                start_date= self.start_date, 
                                end_date = self.end_date,
                                active = False )
            another_sale.save()

    def test_not_valid_if_brand_is_missing(self):
        with self.assertRaises(IntegrityError):
            another_sale = Sale(category = self.category,company = self.company,
                                model="proair", min_quantity = 2,
                                unit_of_measure = "pcs",price_in_inr = 24000,
                                new = True, refurbished = True, warranty = 24,
                                start_date= self.start_date, 
                                end_date = self.end_date,
                                active = False )
            another_sale.save()

    def test_not_valid_is_active(self):
        another_sale = Sale(category = self.category,company = self.company,
                            model="proair", min_quantity = 2,
                            brand = self.brand,
                            unit_of_measure = "pcs",price_in_inr = 24000,
                            new = True, refurbished = True, warranty = 24,
                            start_date= self.start_date + datetime.timedelta(days = DEFAULT_SALE_TIME), 
                            end_date = self.end_date,
                            active = False )
        self.assertFalse(another_sale.is_active)


class TestPushNotificationModel(unittest.TestCase):
    def setUp(self):
        self.state, result = State.objects.get_or_create(name='Karnataka', short_name='KA')
        self.city, result = City.objects.get_or_create(name='Bangalore', state=self.state)
        self.company, result = Company.objects.get_or_create(name='Microsoft', address_line_1='Somewhere',
                                                             city=self.city, state=self.state,
                                                             pin_code='560010', landline_number='080-35353534',
                                                             tin='1111111',
                                                             tan='111111111', service_tax_number='11111111')
        self.user, result = User.objects.get_or_create(email = "test@123.com", mobile_no="123123",
                                                       password = "trial123", is_staff=True,
                                                       is_superuser=False, company=self.company)
        self.push_notification, result = PushNotification.objects.get_or_create(user=self.user,
                                                                           gcm_id = "abc123",
                                                                           imei_no="329478",
                                                                           phone_no="123123",
                                                                           mobile_make="Nokia",
                                                                           mobile_model="abc123",
                                                                           os_version = "os5",
                                                                           app_version = 3.02)
    def test_a_valid_push_notification(self):
        self.assertEqual(self.push_notification.user, self.user)
        self.assertEqual(self.push_notification.gcm_id,"abc123")
        self.assertEqual(self.push_notification.imei_no,"329478")
        self.assertEqual(self.push_notification.phone_no,"123123")
        self.assertEqual(self.push_notification.mobile_make,"Nokia")
        self.assertEqual(self.push_notification.mobile_model,"abc123")
        self.assertEqual(self.push_notification.os_version,"os5")
        self.assertEqual(self.push_notification.app_version,3.02)

    def test_not_vaild_if_user_is_missing(self):
        with self.assertRaises(IntegrityError):
            another_push_notification = PushNotification.objects.get_or_create(gcm_id = "abc123",
                                                                               imei_no="329478",
                                                                               phone_no="123123",
                                                                               mobile_make="Nokia",
                                                                               mobile_model="abc123",
                                                                               os_version = "os5",
                                                                               app_version = 3.02)
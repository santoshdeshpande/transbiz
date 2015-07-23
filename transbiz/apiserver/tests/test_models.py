import unittest
import datetime
from django.db import IntegrityError
from ..models import City, State, IndustryVertical, Category, SubscriptionPlan, Company, Subscription


class TestCityModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_city_does_not_allow_duplicate_names(self):
        self.state = State.objects.create(name='Karnataka', short_name='KA')
        city = City.objects.create(name='Bangalore', state=self.state)
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

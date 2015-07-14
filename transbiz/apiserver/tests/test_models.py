import unittest
from django.db import IntegrityError
from ..models import City, State, IndustryVertical


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
        vertical = IndustryVertical.objects.create(name='Infotech')
        self.assertEqual(vertical.active, True)
        self.assertEqual(vertical.description, None)
        self.assertEqual(vertical.name, 'Infotech')

    def test_duplicate_names_are_not_allowed(self):
        with self.assertRaises(IntegrityError):
            IndustryVertical.objects.create(name='Infotech')
            IndustryVertical.objects.create(name='Infotech')



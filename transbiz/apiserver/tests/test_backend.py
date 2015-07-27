import unittest
from ..models import Company, User
from ..auth_backends import MobileAuthBackend
from model_mommy import mommy

class TestMobileAuthBackend(unittest.TestCase):
    def setUp(self):
        company = Company.objects.get(pk=1)
        self.user1, result = User.objects.get_or_create(email='aaa@aaa.com', mobile_no='999', company=company)
        self.user1.set_password('test123')
        self.user1.save()
        self.backend = MobileAuthBackend()

    def test_backend_returns_invalid_when_no_subscription(self):
        company = mommy.make(Company)
        self.user2, result = User.objects.get_or_create(email='aba@aaa.com', mobile_no='9990', company=company)
        self.user2.set_password('test123')
        self.user2.save()
        user = self.backend.authenticate(email='9990', password='test123')
        self.assertIsNone(user)

    def test_backend_checks_with_mobile_number(self):
        user = self.backend.authenticate(email='999', password='test123')
        self.assertIsNotNone(user)
        self.assertEqual(self.user1.email, user.email)

    def test_backend_throws_does_not_exist(self):
        # with self.assertRaises(userModel.DoesNotExist):
        user = self.backend.authenticate(email='999765', password='test123')
        self.assertIsNone(user)


from django.test import TestCase
from users.models import User, Profile
from django.test import Client


class ModelsTest(TestCase):
    """
    Test for custom User model and Profile model.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='TESTuser9876', email='testemail@gmail.com', first_name='test', last_name='test', password='randomPassword2468')
        c = Client()
        c.login(username=self.user.username, password='randomPassword2468')
        self.profile = Profile.objects.get(user=self.user.id)
        self.profile.phone = '09125467896'
        self.profile.address = 'myaddress'
        self.profile.receive_updates = True

    def test_user(self):
        self.assertEqual(self.user.username, 'TESTuser9876')
        self.assertEqual(self.user.email, 'testemail@gmail.com')
        self.assertEqual(self.user.first_name, 'test')
        self.assertEqual(self.user.last_name, 'test')

    def test_profile(self):
        self.assertEqual(self.profile.phone, '09125467896')
        self.assertEqual(self.profile.address, 'myaddress')
        self.assertEqual(self.profile.receive_updates, True)
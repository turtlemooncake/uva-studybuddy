from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

# SAMPLE TEST CASES 
class UserTestCase(TestCase):
    def test_user(self):
        username = 'studybuddy'
        password = 'buddystudy'
        u = User(username=username)
        u.set_password(password)
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))



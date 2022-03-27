from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
# Create your tests here.

class ProfileTestCase(TestCase):
    def test_profileFirstName(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='')
        self.assertEqual(profUser.user.first_name, 'vic')

    def test_profileLastName(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='')
        self.assertEqual(profUser.user.last_name, 'li')

    def test_profileLastNameIncorr(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='')
        self.assertNotEqual(profUser.user.first_name, 'jessica')

    def test_profileBio(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='here is a pond. it is blue.')
        self.assertEqual(profUser.about, 'here is a pond. it is blue.')
    
    def test_profileBioIncorr(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='here is a pond. it is blue.')
        self.assertNotEqual(profUser.about, 'here is a pond. it is purple')
    
    def test_profileMajor(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='', major='CS')
        self.assertEqual(profUser.major, 'CS')
    
    def test_profileMajorIncorr(self):
        myUser = User(first_name='vic', last_name='li')
        profUser = Profile(user=myUser, about='', major='CS')
        self.assertNotEqual(profUser.major, 'Music')
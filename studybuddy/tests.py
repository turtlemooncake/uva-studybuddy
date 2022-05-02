from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Course
from .forms import EditProfileForm
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
    
class CourseTestCase(TestCase):
    def test_courseCreationAbbv(self):
        newCourse = Course(courseAbbv='CS', courseNumber='1110', courseTitle='Introduction to Programming', courseTopic='topical')
        self.assertEqual(newCourse.courseAbbv, 'CS')
    
    def test_courseCreationNumber(self):
        newCourse = Course(courseAbbv='CS', courseNumber='1110', courseTitle='Introduction to Programming', courseTopic='topical')
        self.assertEqual(newCourse.courseNumber, '1110')
    
    def test_courseCreationTitle(self):
        newCourse = Course(courseAbbv='CS', courseNumber='1110', courseTitle='Introduction to Programming', courseTopic='topical')
        self.assertEqual(newCourse.courseTitle, 'Introduction to Programming')
    
    def test_courseCreationTopice(self):
        newCourse = Course(courseAbbv='CS', courseNumber='1110', courseTitle='Introduction to Programming', courseTopic='topical')
        self.assertEqual(newCourse.courseTopic, 'topical')
    

class ProfileCourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(courseAbbv='CS', courseNumber='1110', courseTitle='Introduction to Programming', courseTopic='topical')
        Course.objects.create(courseAbbv='CS', courseNumber='2150', courseTitle='Programming and Data Representation', courseTopic='topical')
        User.objects.create(first_name='vic', last_name='li')
        Profile.objects.create(user=User.objects.get(first_name='vic'), about='', major='CS')

    def test_addCourseToProfile(self):
        myProf = Profile.objects.get(major='CS')
        myCourse = Course.objects.get(courseNumber='2150')
        myProf.courses.add(myCourse)
        self.assertEqual(myProf.courses.get(courseNumber='2150'), myCourse)
    
    def test_NotFoundCourseInProfile(self):
        myProf = Profile.objects.get(major='CS')
        myCourse = Course.objects.get(courseNumber='2150')
        otherCourse = Course.objects.get(courseNumber='1110')
        myProf.courses.add(myCourse)
        self.assertNotEqual(myProf.courses.get(courseNumber='2150'), otherCourse)

class ProfileEditTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='vic', last_name='li')
        Profile.objects.create(user=User.objects.get(first_name='vic'), about='', major='CS')
    
    def test_ChangeProfileMajor(self):
        myProfile = Profile.objects.all().first()
        myProfile.major = 'Commerce'
        self.assertEqual('Commerce', myProfile.major)
    
    def test_ChangeProfileAbout(self):
        myProfile = Profile.objects.all().first()
        myProfile.about = 'this is about'
        self.assertEqual('this is about', myProfile.about)
    
    def test_ChangeProfileBothFieldsTogether(self):
        myProfile = Profile.objects.all().first()
        myProfile.major = 'Commerce'
        myProfile.about = 'this is about'
        myUser = User(first_name='victoria', last_name='liiii')
        changedProfile = Profile(user=myUser, about='this is about', major='Commerce')
        self.assertEqual(changedProfile.major, myProfile.major)
        self.assertEqual(changedProfile.about, myProfile.about)


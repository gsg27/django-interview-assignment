from django.urls import include, path, reverse
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase
from LibraryApp.models import User

# from rest_framework_simplejwt.tokens import RefreshToken


def create_user(self):
    self.client = APIClient()
    self.user = User(first_name='test_user',last_name='test',email=
    'test@gmail.com',username='test',password="abc123",is_librarian=True,is_member=False)
    self.user.set_password("abc123")
    self.user.save()
    self.data = {'username':'test','password':"abc123"}
    



class TestCase(APITestCase):
 
    @classmethod
    def setUp(self):
        # SetUp required environment for tests
        create_user(self)
        
 
 
    def tests(self):
           
        url = reverse('token_obtain')
        response = self.client.post(url,self.data)
        resp = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + resp['access'])
        self.assertEqual(response.status_code,200)

        url = reverse('token_refresh')  
        response = self.client.post(url,{'refresh':resp['refresh']})
        self.assertEqual(response.status_code,200)

        url = reverse('members')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

        
    
    def tearDown(self):
        # Clean up after each test
        self.user.delete()



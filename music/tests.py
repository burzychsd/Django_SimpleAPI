from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Song
from .serializers import SongsSerializer
import simplejson as json



# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title='', artist=''):
        if title != '' and artist != '':
            Song.objects.create(title=title, artist=artist)
    
    def login_a_user(self, username='', password=''):
        url = reverse(
            'auth-login',
            kwargs={
                'version': 'v1'
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username='test_user',
            email='test@gmail.com',
            password='testing',
            first_name='test',
            last_name='user',
        )
        # test data
        self.create_song('like glue', 'sean paul')
        self.create_song('hey jude', 'the beatles')
        self.create_song('for once in my life', 'stevie wonder')
    
    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token
    
class GetAllSongsTest(BaseViewTest):
    def test_get_all_songs(self):
        self.login_client('test_user', 'testing')
        response = self.client.get(
            reverse('songs-all', kwargs={'version': 'v1'})
        )
        expected = Song.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AuthLoginUserTest(BaseViewTest):
    def test_login_user(self):
        response = self.login_a_user('test_user', 'testing')
        # assert token key exists
        self.assertIn('token', response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #test login with invalid credentials
        response = self.login_a_user('annonymous', 'pass')
        #assert status code is 40 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthRegisterUserTest(BaseViewTest):
    def test_register_user(self):
        url = reverse(
            'auth-register',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                'username': 'new_user',
                'password': 'new_pass',
                'email': 'new_user@gmail.com'
            }),
            content_type='application/json'
        )
        # assert status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_invalid_data(self):
        url = reverse(
            "auth-register",
            kwargs={
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "",
                    "password": "",
                    "email": ""
                }
            ),
            content_type='application/json'
        )
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

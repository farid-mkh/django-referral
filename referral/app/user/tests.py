from django.urls import reverse
from rest_framework import test, status

from user.models import User

from rest_framework_simplejwt.tokens import RefreshToken

SAMPLE_DATA = {
    "first_name": "farid",
    "family_name": "mokhtari",
    "email": "farid.mkhtri@gmail.com"
}

class TestUsers(test.APITestCase):

    # def register
    def test_register(self):
        """Test user registering"""
        response = self.client.post(reverse("register"),data={"mobile_number":"09900000000", "password": "test123"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_user_detail_without_auth(self):
        """Test user detail without authentication"""
        response = self.client.get(reverse("user-detail"))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
        
        
class TestAuth(test.APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile_number="09900000000",password="Farid1376")
        self.refresh = RefreshToken.for_user(self.user)
    
    def test_user_detail_auth(self):
        """Test user detail with authentication"""
        response = self.client.get(reverse("user-detail"),HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_update_user(self):
        """Test updating user"""
        response = self.client.put(reverse("update-profile"),
                                   data=SAMPLE_DATA,
                                   HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
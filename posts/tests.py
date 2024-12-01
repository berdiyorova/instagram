from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import PostModel
from users.models import UserModel


class PostModelTests(APITestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.post_data = {
            "caption": "This is a test post"
        }

    def test_create_post(self):
        response = self.client.post("/posts/", data=self.post_data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostModel.objects.count(), 1)

    # def test_get_post_list(self):
    #     # Create a post first
    #     self.client.post(reverse('postmodel-list'), data=self.post_data)
    #     response = self.client.get(reverse('postmodel-list'))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

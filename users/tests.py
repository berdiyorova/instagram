# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import UserModel, AuthType
#
#
# class RegisterViewTests(APITestCase):
#
#     def setUp(self):
#         self.url = reverse('register')  # Ensure the URL name matches your configuration
#
#     def test_register_with_email(self):
#         # Test registering a user with email
#         data = {
#             'email_or_phone': 'testuser@example.com',
#             'auth_type': AuthType.VIA_EMAIL,
#         }
#
#         response = self.client.post(self.url, data)
#
#         # Verify success and appropriate response
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(UserModel.objects.count(), 1)
#         user = UserModel.objects.first()
#         self.assertEqual(user.email, 'testuser@example.com')
#         self.assertEqual(user.auth_type, AuthType.VIA_EMAIL)
#
#     def test_register_with_phone(self):
#         # Test registering a user with phone
#         data = {
#             'email_or_phone': '+998338009095',
#             'auth_type': AuthType.VIA_PHONE,
#         }
#
#         response = self.client.post(self.url, data)
#
#         # Verify success and appropriate response
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(UserModel.objects.count(), 1)
#         user = UserModel.objects.first()
#         self.assertEqual(user.phone, '+998338009095')
#         self.assertEqual(user.auth_type, AuthType.VIA_PHONE)
#

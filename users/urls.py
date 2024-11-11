from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify/', views.VerifyView.as_view()),
    path('verify/resend/', views.ResendVerifyView.as_view()),
]

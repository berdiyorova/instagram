from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify/', views.VerifyView.as_view()),
    path('verify/resend/', views.ResendVerifyView.as_view()),
    path('change/', views.ChangeUserInformationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('following/', views.FollowingView.as_view()),
]

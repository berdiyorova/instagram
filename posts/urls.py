from django.urls import path

from posts import views

urlpatterns = [
    path('list/', views.PostListView.as_view()),
    path('create/', views.PostCreateView.as_view()),
    path('<uuid:pk>/', views.PostDetailView.as_view()),
]

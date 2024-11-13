from django.urls import path
from rest_framework.routers import DefaultRouter

from posts import views

router = DefaultRouter()
router.register(prefix=r'', viewset=views.PostViewSet)
router.register(prefix=r'comments', viewset=views.CommentViewSet)

urlpatterns = [
    path('like/', views.PostLikeView.as_view()),
    path('comments/like/', views.CommentLikeView.as_view()),
] + router.urls

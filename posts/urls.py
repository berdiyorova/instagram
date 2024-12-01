from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts import views

router = DefaultRouter()
router.register(prefix=r'posts', viewset=views.PostViewSet, basename='posts')
router.register(prefix=r'comments', viewset=views.CommentViewSet)

urlpatterns = [
    path('like/', views.PostLikeView.as_view(), name='post-like'),
    path('comments/like/', views.CommentLikeView.as_view()),
    path('', include(router.urls)),
]

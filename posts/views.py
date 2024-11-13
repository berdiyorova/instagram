from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.permissions import IsOwnerOrReadOnly
from posts.models import PostModel, CommentModel, PostLikeModel, CommentLikeModel
from posts.serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = PostModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = CommentModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeView(APIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        author = self.request.user
        post = serializer.validated_data['post']

        data = {"success": True}
        like = PostLikeModel.objects.filter(author=author, post=post)

        if like.exists():
            like.delete()
            data["message"] = f"You have disliked this post."

            return Response(data=data, status=status.HTTP_204_NO_CONTENT)

        PostLikeModel.objects.create(author=author, post=post)
        data["message"] = f"You have liked this post."

        return Response(data=data, status=status.HTTP_201_CREATED)



class CommentLikeView(APIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        author = self.request.user
        comment = serializer.validated_data['comment']

        data = {"success": True}
        like = CommentLikeModel.objects.filter(author=author, comment=comment)

        if like.exists():
            like.delete()
            data["message"] = f"You have disliked this comment."

            return Response(data=data, status=status.HTTP_204_NO_CONTENT)

        CommentLikeModel.objects.create(author=author, comment=comment)
        data["message"] = f"You have liked this comment."

        return Response(data=data, status=status.HTTP_201_CREATED)

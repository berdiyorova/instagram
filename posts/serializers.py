from rest_framework import serializers

from posts.models import PostModel, PostLikeModel, CommentModel, CommentLikeModel


class PostSerializer(serializers.ModelSerializer):
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    me_liked = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = PostModel
        fields = (
            "id",
            'author',
            'image',
            'caption',
            'created_at',
            "post_likes_count",
            "post_comments_count",
            "me_liked"
        )
        extra_kwargs = {
            "image": {"required": False},
            "author": {"read_only": True}
        }

    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_post_comments_count(obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            if PostLikeModel.objects.filter(post=obj, author=request.user).exists():
                return True

        return False


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    me_liked = serializers.SerializerMethodField('get_me_liked')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    class Meta:
        model = CommentModel
        fields = [
            "id",
            "author",
            "comment",
            "post",
            "parent",
            "created_time",
            "replies",
            "me_liked",
            "likes_count",
          ]
        extra_kwargs = {
            "author": {"read_only": True}
        }

    def get_replies(self, obj):
        if obj.child.exists():
            serializer = self.__class__(obj.child.all(), many=True, context=self.context)
            return serializer.data
        else:
            return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        else:
            return False

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()



class CommentLikeSerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=CommentModel.objects.all())

    class Meta:
        model = CommentLikeModel
        fields = ("id", "author", "comment")
        extra_kwargs = {
            "author": {"read_only": True}
        }


class PostLikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=PostModel.objects.all())

    class Meta:
        model = PostLikeModel
        fields = ("id", "author", "post")
        extra_kwargs = {
            "author": {"read_only": True}
        }

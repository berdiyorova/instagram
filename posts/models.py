from django.db import models

from common.models import BaseModel
from users.models import UserModel


class PostModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    caption = models.TextField()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.author} post about {self.caption}"



class CommentModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"comment by {self.author}"



class PostLikeModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('author', 'post')



class CommentLikeModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('author', 'comment')

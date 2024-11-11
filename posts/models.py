from django.db import models

from common.models import BaseModel
from users.models import UserModel


class PostModel(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.author} post about {self.caption}"

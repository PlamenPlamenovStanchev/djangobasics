from django.db import models

from posts.choises import LanguageChoices
from posts.validators import BadWordsValidator


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(
        validators=[BadWordsValidator(
            bad_words=[
                "fuck", "shit", "ass", "vagina"
            ]
        )]
    )
    author = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)
    programming_language = models.CharField(max_length=20,
                                            choices=LanguageChoices.choices,
                                            default=LanguageChoices.OTHER,
                                            )
    image = models.ImageField(upload_to='media-files/', blank=True, null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



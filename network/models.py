from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(auto_now=True, blank=True)
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    def num_likes(self):
        return self.liked.all().count()

    def __str__(self):
        return f"{self.user} posted on : {self.date}"

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)
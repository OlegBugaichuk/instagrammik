from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    about = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='users/avatars', default=None)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return str(self.user.username)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='users/posts/images')
    date_pub = models.DateTimeField(default=timezone.now)
    data_edit = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='users_likes_it', blank=True)

    @property
    def get_likes(self):
        return self.likes.count()

    def __str__(self):
        return 'Post #{0}, author - {1} '.format(self.id, self.author.username)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_pub = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Author - {0}, Post - {1}'.format(self.author.username, self.in_post.id)

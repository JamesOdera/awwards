from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    author = models.ForeignKey(User,  on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        ordering = ['-id']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].author)
    kwargs['instance'].slug = slug


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.post.title + ' Image'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Profile of User {}".format(self.user.username)

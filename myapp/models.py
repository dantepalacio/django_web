from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation



class CustomUser(User):
    pass


class Token(models.Model):
    objects = models.Manager()


class Publisher(models.Model):
    question = models.TextField()


class Arcticle(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Автор', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    text = models.TextField(verbose_name='Текст статьи')
    # likes = models.ForeignKey(Like, related_name='liked_articles')


    def __str__(self):
        return self.name
    
    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'


User.add_to_class("total_likes", lambda self: sum(arcticle.total_likes() for arcticle in self.arcticle_set.all()))



class Like(models.Model):
    user = models.ForeignKey(User,related_name='likes', on_delete=models.CASCADE)
    arcticle = models.ForeignKey(Arcticle, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

 

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/')
    instagram = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=False, verbose_name='profile status')


class Comments(models.Model):
    arcticle = models.ForeignKey(Arcticle, on_delete= models.CASCADE, verbose_name='Статья', blank=True, null=True, related_name='comments_arcticle')
    author = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    date = models.DateField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(default = False, verbose_name='Видимость комментария')




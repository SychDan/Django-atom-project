from django.db import models
from django.conf import settings
from django import db
from django.urls import reverse
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.auth.models import AbstractUser

class Wall(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name=models.CharField(max_length=50, db_index=True)
    place=models.ForeignKey('Place', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.place_id)

class Place(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    town=models.CharField(max_length=50, db_index=True)
    state=models.ForeignKey('State', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s %s' % (self.town, self.state_id)

class State(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name=models.CharField(max_length=50, db_index=True)

    def __unicode__(self):
        return u'%s' % (self.name)



class Person(AbstractUser):
    #id = models.AutoField(primary_key=True, db_index=True)
    #nickname=models.CharField(max_length=50, unique=True)
    #email=models.EmailField(max_length=50)
    #password=models.CharField(max_length=50)
    #REQUIRED_FIELDS=['email','password']
    #USERNAME_FIELD='nickname'
    #PASSWORD_FIELD='password'
    pass


class Post(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    title=models.CharField(max_length=50, db_index=True)
    message=models.TextField()
    publication_date=models.DateTimeField(auto_now_add=True)
    person=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Wall=models.ForeignKey('Wall', on_delete=models.CASCADE)
    vote = GenericRelation('LikeDislike', related_query_name='post')

    def get_absolute_url(self):
        return reverse('post',args=[str(self.id)])


class Theme(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    post=models.ManyToManyField(Post)
    name=models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % (self.name)


class Comment(models.Model):
    message=models.TextField(max_length=300)
    publication_date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey('Post', on_delete=models.CASCADE)
    person=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote=GenericRelation('LikeDislike',related_query_name='comment')
    def __unicode__(self):
        return u'%s %s %s %s' % (self.message, self.person_id, self.publication_date, self.post_id)



class LikeDislikeManager(db.models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def posts(self):
        return self.get_queryset().filter(content_type__model='post')

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment')

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
    objects = LikeDislikeManager()
    vote = models.SmallIntegerField(choices=VOTES)
    person=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    def __unicode__(self):
        return u'%s %s' % (self.person_id, self.vote)

    class Meta:
        unique_together = (("content_type","object_id", "person"),)
from django import template
from Atom.models import LikeDislike,Post,Comment
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.db import connection
register=template.Library()

@register.simple_tag
def postLikeDislike(pk):
    cursor = connection.cursor()
    sum = cursor.execute('select SUM(vote) from Atom_likedislike where object_id=(%s) and content_type_id=12' % pk)
    row = cursor.fetchone()
    return row[0]

@register.simple_tag
def commentLikeDislike(pk):
    cursor=connection.cursor()
    sum=cursor.execute('select SUM(vote) from Atom_likedislike where object_id=(%s) and content_type_id=10' % pk)
    row = cursor.fetchone()
    return row[0]
        #LikeDislike.objects.filter(content_type_id=ContentType.objects.get_for_model(Comment.objects.get(id=pk)).id,object_id=Comment.objects.get(id=pk).id).aggregate(Sum('vote')).get('vote__sum')


@register.simple_tag
def countPosts(pk):
    cursor = connection.cursor()
    count = cursor.execute('select COUNT(id) FROM Atom_post where Wall_id=(%s)' % pk)
    #count=Post.objects.raw('select SUM(id) FROM Atom_post where Wall_id=(%s)' % pk)
    #count=Post.objects.filter(Wall_id=pk).count()
    row=cursor.fetchone()
    return row[0]

@register.simple_tag
def countComments(pk):
    cursor = connection.cursor()
    count = cursor.execute('select COUNT(id) FROM Atom_comment where post_id=(%s)' % pk)
    #count=Post.objects.raw('select SUM(id) FROM Atom_post where Wall_id=(%s)' % pk)
    #count=Post.objects.filter(Wall_id=pk).count()
    row=cursor.fetchone()
    return row[0]

@register.simple_tag
def countCommentsTheme(pk):
    cursor = connection.cursor()
    count = cursor.execute('SELECT count(*) FROM database_for_joe.Atom_theme_post where theme_id=(%s)' % pk)
    #count=Post.objects.raw('select SUM(id) FROM Atom_post where Wall_id=(%s)' % pk)
    #count=Post.objects.filter(Wall_id=pk).count()
    row=cursor.fetchone()
    return row[0]
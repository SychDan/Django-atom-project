import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Joe.settings'
django.setup()
from django.contrib.contenttypes.models import ContentType
from Atom.models import Post,Comment,Wall,State,Place,Theme, LikeDislike
from django.contrib.auth.models import AbstractUser,User
from django.contrib.auth import get_user_model
from django.db.models import Avg, Max, Min ,Sum, Count
from django.contrib.auth.hashers import make_password
from hashlib import sha256
from django.utils.crypto import (
    pbkdf2, get_random_string)
import base64
from Atom.models import Person
"""""
name=[]
nick=[]
import random as r
ss=open('themes.txt','r')
trends=[]
for i in ss:
    trends.append(i)
output = []
i=0
i+=1
ff=open('themes.txt','w')
for x in trends:
    if x not in output:
        output.append(x)
        i+=1
        r=i
        print(r)
        ff.write(x)

print(output.__len__())
"""""
from Atom.models import Person

#p=Person(username="danya",password="12345".__hash__(),email="sisiska@yandex.ru")
#p.save()
#print(sha256("12345".encode("UTF-8")).hexdigest())

#password = '12345'
#algorithm = "pbkdf2_sha256"
#iterations = 20000
#salt = 'w5Pl4a33Ygp9'
#digest = sha256
#hash = pbkdf2(password, salt, iterations, digest=digest)
#hash = base64.b16encode(hash).strip()
#print("%s$%d$%s$%s" % (algorithm, iterations, salt, hash))
#print(hash)
#User=get_user_model()
#user=User.objects.create_user(username="Loly",email="efeff@yandex.ru", password="12345")
#user.save()
#obj=State(name="Russia2")
#obj.save()
#obj=Place(state_id=2,town="Moscow2")
#obj.save()
#obj=Wall(place_id=2,name="Anything2")
#obj.save()
#obj=Post(title="23tpogrst2",message="Stay hungry, stay foolish", person_id=2,Wall_id=2)
#obj.save()
#for value in Post.objects.filter(person_id=2).filter():
#     print(value.title)
#p = ContentType.objects.get(app_label="Atom", model="Post")
#print(p)
#us=get_user_model()
#user=us.objects.get(id=80161)
#print(user.username)
poswt=Post.objects.all()[:10]
for post in poswt:
    conty=ContentType.objects.get_for_model(post)
    oblist=LikeDislike.objects.filter(content_type__pk=conty.pk, object_id=post.pk).aggregate(Sum('vote')).get('vote__sum')
#if oblist!=None:
#    for i in oblist:
#        print(i)
    print(oblist)
print('Second tour')
p=LikeDislike.objects.filter(content_type_id=ContentType.objects.get_for_model(Post.objects.get(pk=222)).id,object_id=Post.objects.get(pk=222).id).aggregate(Sum('vote'))
print(p)
pc=Comment.objects.get(pk=2222)
pp=LikeDislike.objects.comments()
from  django.db import connection
corsor=connection.cursor()
print(corsor.execute('select SUM(vote) from Atom_likedislike where object_id=(%s)' %3))
#user=Person.object.create_user()
print(Person.objects.filter(username__contains='vi'))
Model=Post
model = Model.objects.filter(title__contains="r").annotate(cc=Sum('vote__vote'))
print(model[0].cc)
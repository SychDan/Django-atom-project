import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from Atom.models import Post,Person,Place,Comment,LikeDislike,Wall,Theme,State
import random as r
import time


states=[]
towns=[]
nicknames=[]
emails=[]
themes=[]
passwords=[]
comments=[]
amwords=[]
votes=[1,-1]

start_time=time.time()

def openAllFiles():
    f=open('support/States.txt','r')
    for i in f:
        states.append(i.split('\n')[0])
    f.close()
    f=open('support/nickname2.txt','r')
    for i in f:
        nicknames.append(i.split('\n')[0])
    f.close()
    f=open('support/americanTown.txt','r')
    for i in f:
        towns.append(i.split('\n')[0])
    f.close()
    f=open('support/Emails.txt','r')
    for i in f:
        emails.append(i.split('\n')[0])
    f.close()
    f=open('support/Passwords.txt','r')
    for i in f:
        passwords.append(i.split('\n')[0])
    f.close()
    f=open('support/themes.txt','r')
    for i in f:
        themes.append(i.split('\n')[0])
    f.close()
    f=open('support/engcomment.txt','r')
    for i in f:
        comments.append(i.split('\n')[0])
    f.close()
    f=open('support/amword.txt','r')
    for i in f:
        amwords.append(i.split('\n')[0])
    f.close()

def getFromDB():
    f=Person.objects.values_list("username","email","password")
    for value in f:
        nicknames.append(value[0])
        emails.append(value[1])
        passwords.append(value[2])
    f=State.objects.values_list("name")
    for i in f:
        states.append(i[0])
    f=Place.objects.values_list("town")
    for i in f:
        towns.append(i[0])
    f=Wall.objects.values_list("name")
    for i in f:
        amwords.append(i[0])
    f=Theme.objects.values_list("name")
    for i in f:
        themes.append(i[0])
    f=Comment.objects.values_list("message")
    for i in f:
        comments.append(i[0])


def clean():
    worktime = time.time()
    Post.objects.all().delete()
    print('Posts were deleted, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    Person.objects.all().delete()
    print('Persons were deleted, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    Place.objects.all().delete()
    print('Places were deleted, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    Comment.objects.all().delete()
    print('Comments were deleted, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    Theme.objects.all().delete()
    print('Themes were deleted, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    State.objects.all().delete()
    print('States were deleted, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    Wall.objects.all().delete()
    print('Walls were deleted, time: {0}'.format(time.time() - worktime))


def toDataBase():
    print('{0} nicknames left after groupby'.format(nicknames.__len__()))
    print('Filling in!')
    worktime = time.time()
    obj=(State(name=i) for i in states)
    State.objects.bulk_create(obj)
    print('States were added, time: {0}'.format(time.time()-worktime))
    worktime = time.time()
    model=[]
    for i in State.objects.values_list("id"):
        model.append(i[0])
    obj=(Place(town=i, state_id=r.choice(model)) for i in towns)
    Place.objects.bulk_create(obj)
    print('Places were added, time: {0}'.format(time.time()-worktime))
    worktime = time.time()
    model.clear()
    for i in Place.objects.values_list("id"):
        model.append(i[0])
    obj = (Wall(name=i,place_id=r.choice(model)) for i in amwords)
    Wall.objects.bulk_create(obj)
    print('Walls were added, time: {0}'.format(time.time()-worktime))
    worktime = time.time()
    obj = (Person(username=i, email=r.choice(emails),password=r.choice(passwords)) for i in nicknames)
    Person.objects.bulk_create(obj)
    print('Persons were added, time: {0}'.format(time.time()-worktime))
    worktime = time.time()
    model.clear()
    for i in Person.objects.values_list("id"):
        model.append(i[0])
    model2 = []
    for i in State.objects.values_list("id"):
        model2.append(i[0])
    obj = (Post(title=r.choice(amwords), message=r.choice(comments),person_id=r.choice(model),Wall_id=r.choice(model2)) for i in range(100000))
    Post.objects.bulk_create(obj)
    allFromPost=Post.objects.all()
    print('Posts were added, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    obj=(LikeDislike(content_object=i,person_id=r.choice(model),vote=r.choice(votes)) for i in allFromPost)
    LikeDislike.objects.bulk_create(obj)
    print('Likes and dislikes for post were added, time: {0}'.format(time.time()-worktime))
    worktime = time.time()
    obj = (Theme(name=i) for i in themes)
    Theme.objects.bulk_create(obj)
    a=Theme.post.through
    idtheme=[]
    for i in Theme.objects.values_list("id"):
        idtheme.append(i[0])
    idpost=[]
    for i in Post.objects.values_list("id"):
        idpost.append(i[0])
    vv=(a(theme_id=r.choice(idtheme), post_id=i) for i in idpost)
    a.objects.bulk_create(vv)
    print('Themes were added, time: {0}'.format(time.time() - worktime))
    worktime = time.time()
    model2.clear()
    for i in Post.objects.values_list("id"):
        model2.append(i[0])
    obj = (Comment(message=i,person_id=r.choice(model),post_id=r.choice(model2)) for i in comments)
    Comment.objects.bulk_create(obj)
    print('Comments were added, time: {0}'.format(time.time() - worktime))
    allFromComm=Comment.objects.all()
    worktime = time.time()
    obj = (LikeDislike(content_object=i, person_id=r.choice(model), vote=r.choice(votes)) for i in allFromComm)
    LikeDislike.objects.bulk_create(obj)
    print('Likes and dislikes for comments were added, time: {0}'.format(time.time()-worktime))

#clean()
openAllFiles()
#getFromDB()
toDataBase()

print('That is end, all time: {0}'.format(time.time() - start_time))
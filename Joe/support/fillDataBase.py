import MySQLdb
import random
import re
def X():
    password=[]
    ww=open('Passwords.txt','w',encoding='UTF-8')
    for i in range(100000):
        x=""
        for j in range(random.randint(5,15)):
           x=x+chr(random.randint(97,122))
        ww.write(x+'\n')
        password.append(x)
    for i in password:
        print(i)
def Y():
    post=[]
    ww=open('Emails.txt','w',encoding='UTF-8')
    ss=open('nickname.txt','r')
    aa=open('postt','r')
    for i in aa:
        post.append(i.split('\n')[0])
    for i in ss:
        ww.write(str(i.split('\n')[0])+"@"+random.choice(post)+'\n')
    ww.close()
    ww=open('Emails.txt','r',encoding='UTF-8')
    for i in ww:
        print(i.split('\n')[0])
def Z():
    ee=[]

    ww=open('tags.txt','w')

    tt=open('tags','r')
    for i in tt:
        j=i.split('#')
        for k in j:
            j1=k.split('\n')
            for s in j1:
                j2=s.split(' ')
                for d in j2:
                    ee.append(d)

    for i in ee:
        ww.write(i+'\n')
    ww.close()
    ww = open('tags.txt', 'r')
    for i in ww:
        print(i)
def A():
    rr=[]
    aa=open('tags.txt','r')
    ww=open('themes.txt','w')
    for i in aa:
        rr.append(i)
    zz = list(filter(lambda x: x != '\n', rr))
    for i in zz:
        ww.write(i)

def B():
    aa=open('amword','r')
    bb=open('amwords.txt','w',encoding='utf-8')
    for i in aa:

        bb.write(i.split(' ')[0]+'\n')

B()
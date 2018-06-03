from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.urls import reverse, resolve
from django.db.models import Q
import json
from django.http import JsonResponse, Http404
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from .models import Post,Person, Comment, Wall, State,Theme, LikeDislike
from django.views.generic import ListView, edit, CreateView, View,DetailView
from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from Atom.filter import *
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Min ,Sum, Count, Subquery
from .form import FindForm, Registration, CommentForm, PostForm
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.template.context_processors import csrf,debug

register=template.Library()


def home(request):
    return render(request, 'Atom/home.html', {})


def page(request):
    return render(request, "Atom/page.html")


def out(request):
    logout(request)
    return HttpResponseRedirect('/login/')


class ELoginView(View):

    def get(self, request):
        context = create_context_username_csrf(request)
        return render_to_response('Atom/login.html', context=context)
            
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect('/home/')
        context = create_context_username_csrf(request)
        context['login_form'] = form
        return render_to_response('Atom/login.html', context=context)

def validateUsername(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Person.objects.filter(username__iexact=username).exists(),
        'password2':request.GET.get('password2',None),
        'password':request.GET.get('password',None),
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = AuthenticationForm
    return context


def start(request):
    if auth.get_user(request).is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/login/')


class LoadPosts(ListView):
    model = Post
    context_object_name = "post_list"
    template_name = 'Atom/page.html'
    paginate_by = 5
    #def get_queryset(self):
    #    q=Comment.objects.annotate(num=Count('post_id'))
     #   ww=Post.objects.filter(person_id=self.request.user.id)
    #    return {"q":q,'object'}
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoadPosts, self).get_context_data(**kwargs)
        #content_type = ContentType.objects.get_for_model(Post.objects.get(id=self.object.pk))
        #con = LikeDislike.objects.filter(content_type_id=content_type.id,
        #                                 object_id=Post.objects.get(id=self.object.pk).id)
       # like = con.aggregate(Sum('vote')).get('vote__sum')
        #fff=Post.objects.all().annotate(ccc=Sum('vote__vote')).values('ccc')
        #ddd=Post.objects.all().annotate(xxx=Count('comment')).values('xxx')
        ww = Post.objects.all()[:10].annotate(cc=Sum('vote__vote'))

        context['object']=ww
        return context


    #filter(person_id=self.request.user.id)


class aboutPosts(DetailView,edit.FormMixin):
    model = Post
    purchases_paginate_by = 2
    form_class = CommentForm

    def get_success_url(self):
        return reverse('Atom:post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(aboutPosts, self).get_context_data(**kwargs)
        content_type=ContentType.objects.get_for_model(Post.objects.get(id=self.object.pk))
        con = LikeDislike.objects.filter(content_type_id=content_type.id,object_id=Post.objects.get(id=self.object.pk).id)
        like=con.aggregate(Sum('vote')).get('vote__sum')
        tags=Theme.objects.filter(post__id=self.object.pk)
        mm=Comment.objects.filter(post_id=self.object.pk)
        page = self.request.GET.get('page')
        paginator = Paginator(mm, self.purchases_paginate_by)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context['form']=CommentForm
        context["comments"] = results
        context['like']=like
        context['tags']=tags
        return context

    def post(self,request, *args, **kwargs):
        self.object=self.get_object()
        form=self.get_form()
        if form.is_valid():
            message = form.cleaned_data['message']
            comm = Comment(message=message, person_id=request.user.id, post_id=self.object.pk)
            comm.save()
            print(comm.message)
            return super(aboutPosts,self).form_valid(form)
        else:
            return self.form_invalid(form)


def resultsPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    like=LikeDislike.objects.filter(content_type_id=ContentType.objects.get_for_model(Post.objects.get(id=pk)).id,object_id=Post.objects.get(id=pk).id).aggregate(Sum('vote')).get('vote__sum')
    return render(request, 'Atom/post_detail.html', {'post': post, 'like':like})


def resultsComment(request, pk):
    post = get_object_or_404(Comment, id=pk)
    like=LikeDislike.objects.filter(content_type_id=ContentType.objects.get_for_model(Comment.objects.get(id=pk)).id,object_id=Comment.objects.get(id=pk).id).aggregate(Sum('vote')).get('vote__sum')
    return render(request, 'Atom/post_detail.html', {'post': post, 'like':like})


class LoadComments(ListView):
    model = Comment
    context_object_name = "comm_list"
    template_name = "Atom/comment_list.html"
    paginate_by = 5
    ld=LikeDislike

    #def get_queryset(self):
        #pp=Comment.objects.select_related('post').prefetch_related('person').defer('vote')
    #def get_queryset(self):
        #return pp
    def get_queryset(self):
        return Comment.objects.filter(person_id=self.request.user.id).annotate(cc=Sum('vote__vote'))




class aboutWalls(DetailView):
    model = Wall
    purchases_paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super(aboutWalls, self).get_context_data(**kwargs)
        mm=Post.objects.filter(Wall_id=self.object).order_by('-publication_date')
        page = self.request.GET.get('page')
        self.request.session['[path']=self.request.get_full_path()
        print('yo')
        print(self.request.session['[path'])
        paginator = Paginator(mm, self.purchases_paginate_by)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context["posts"] = mm
        return context


class aboutPerson(DetailView):
    model = Person
    post = Post
    purchases_paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(aboutPerson, self).get_context_data(**kwargs)
        mm = Post.objects.filter(person_id=self.object)
        page = self.request.GET.get('page')
        paginator = Paginator(mm, self.purchases_paginate_by)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context["posts"] = results
        return context


def init(request):
    return render(request, 'Atom/init.html')

def trying(request):
    return render(request, 'Atom/base.html')



@login_required
@require_http_methods(["POST"])
def createPost(request, pk):
    form=PostForm(request.POST)
    post=get_object_or_404(Post,id=pk)
    print(request.method)
    if form.is_valid():
        message=form.cleaned_data['message']
        title=form.cleaned_data['title']
        comm=Post(title=title, message=message, person_id=request.user.id, wall_id=pk)
        comm.save()
        print(comm.message)
        return_path = request.META['HTTP_REFERER']
    return reverse('Atom:wall-detail',kwargs={'pk':pk})

#@csrf_exempt
def search_wall(request):
    model=Wall
    search_field='name'
    return index_person(request,model,search_field)

@csrf_exempt
def search_post(request):
    model = Post
    search_field = 'title'
    return index_person(request, model, search_field)

@csrf_exempt
def search_user(request):
    model=get_user_model()
    search_field = 'username'
    return index_person(request, model, search_field)

@csrf_exempt
def search_theme(request):
    model=Theme
    search_field = 'name'
    return index_person(request, model, search_field)


def simpleRegistration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'Atom/welcome.html')
    else:
        form = Registration()
    return render(request, 'Atom/auth.html', {'form': form})

def welcome(request):
    logout(request)
    return render(request, 'Atom/welcome.html')



class addPost(CreateView):
    model = Post
    template_name = 'Atom/add_post.html'
    fields = ['title','message']
    #success_url = '/profile/'
    form_class = PostForm

    def form_valid(self, form):
        Post.objects.create(message=form.cleaned_data['message'], title=form.cleaned_data['title'],person_id=self.request.user.id,Wall_id=1)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('Atom:theme-detail')



def index_person(request,Model,search_field):
    model = Model.objects.all()
    form = FindForm(request.GET)
    query=request.GET.get('name')
    if query:
        form = FindForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            if(name):
                if search_field=='name':
                    model = model.filter(name__contains = name).annotate(cc=Count('post'))
                elif search_field=='title':
                    model = model.filter(title__contains=name).annotate(cc=Sum('vote__vote'))
                elif search_field == 'username':
                    model = model.filter(username__contains=name).annotate(cc=Count('post'))

    else:
        form = FindForm()
    if search_field == 'name':
        model = model.annotate(cc=Count('post'))
    elif search_field == 'title':
        model = model.annotate(cc=Sum('vote__vote'))
    elif search_field == 'username':
        model = model.annotate(cc=Count('post'))
    paginator = Paginator(model, 7)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    dict = {
        'request':request,
        'message': results,
        'form': form,
    }
    url=''
    if Model==Post:
        url='Atom/search_post.html'
    elif Model==Person:
        url='Atom/search_user.html'
    elif Model==Wall:
        url='Atom/search_wall.html'
    elif Model==Theme:
        url='Atom/search_theme.html'
    return render_to_response(url, dict)

class aboutTheme(DetailView):
    model = Theme
    purchases_paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(aboutTheme, self).get_context_data(**kwargs)
        mm=Post.objects.filter(theme__id=self.object.pk)
        page = self.request.GET.get('page')
        paginator = Paginator(mm, self.purchases_paginate_by)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context["posts"] = results
        return context


def post_list(request):
    numbers_list = Post.objects.filter(person_id=request.user.id).order_by('-publication_date')
    return render_to_response('Atom/post_list.html', {'posts': numbers_list})

def ss(request):
    return render(request,'Atom/dd.html',{'dd':Post.objects.all()[:300]})
def dd(request):
    page = int(request.GET['page'])
    lists = Post.objects.all()[page*10:(page+1)*10]
    return JsonResponse({'dd':list(lists)})


def newbase(request):
    return render(request, 'Atom/newbase.html')

def rest(request):
    return render(request,'Atom/REACT.html')

def contact(request):
    return render(request,'Atom/contact.html')

def faq(request):
    return render(request,'Atom/faq.html')


from django.template.loader import render_to_string
from django.http import JsonResponse

def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = dict()
    if request.method == 'POST':
        post.delete()
        data['form_is_valid'] = True
        posts = Post.objects.filter(person_id=request.user.id).order_by('-publication_date')
        data['html_post_list'] = render_to_string('Atom/CRUD/list.html', {
            'posts': posts
        })
    else:
        context = {'post': post}
        data['html_form'] = render_to_string('Atom/CRUD/delete.html', context, request=request)
    return JsonResponse(data)

def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
    else:
        form = PostForm(instance=post)
    return save_form(request, form, 'Atom/CRUD/update.html')


def save_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            if template_name=='Atom/CRUD/create.html':
                dd=form.save(commit=False)
                dd.person=request.user
                dd.Wall=Wall.objects.get(id=1)
                dd.save()

            else:
                form.save()
            data['form_is_valid'] = True
            post = Post.objects.filter(person_id=request.user.id).order_by('-publication_date')
            data['html_post_list'] = render_to_string('Atom/CRUD/list.html', {
                'posts': post
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form,}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
    else:
        form = PostForm()

    return save_form(request, form, 'Atom/CRUD/create.html')



def indexx(request):
    """ Redirects to index with paginated queryset. """
    people = Person.objects.all()
    text_search = request.GET.get('text_search', '')

    if text_search:
        people = Person.objects.filter(Q(title__contains=text_search))

    paginator = Paginator(people, 20)
    page = paginator.page(1)

    if request.is_ajax():
        page = request.GET.get('page', 1)
        try:
            page = paginator.page(page)
        except:
            raise Http404

        results = {'page': page.number, 'hasNext': page.has_next(),
                   'people': [{'username': person.username,
                               }
                              for person in page.object_list]}
        return JsonResponse(results)

    ctx = {'people': page.object_list, 'text_search': text_search, 'page': page}
    return render(request, 'Atom/dd.html', ctx)


def indexxx(request):
    form = FindForm(request.GET)
    people = Person.objects.all().annotate(cc=Count('post'))
    text_search = request.GET.get('name')
    if text_search:
        people = Person.objects.filter(Q(username__contains=text_search)).annotate(like=Count('post'))
    paginator = Paginator(people, 50)
    page = paginator.page(1)

    if request.is_ajax():
        page = request.GET.get('page', 1)
        try:
            page = paginator.page(page)
        except:
            raise Http404

        results = {'page': page.number, 'hasNext': page.has_next(),
                   'people': [{'username': person.username,
                               'pk':person.pk,

                               'email':person.email
                               }
                              for person in page.object_list]}
        return JsonResponse(results)

    ctx = {'people': page.object_list, 'form': form, 'page': page}
    return render(request, 'Atom/search_user.html', ctx)




def save_formm(request, form, template_name):
    data = dict()
    print('oy')
    print(request.session['[path'][6])
    if request.method == 'POST':
        if form.is_valid():
            dd = form.save(commit=False)
            dd.person = request.user
            dd.Wall = Wall.objects.get(id=request.session['[path'][6])
            dd.save()
            data['form_is_valid'] = True
            post = Post.objects.filter(Wall_id=request.session['[path'][6]).order_by('-publication_date')
            data['html_book_list'] = render_to_string('Atom/CRUD/listWall.html', {
                'posts': post
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form, }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def createm(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
    else:
        form = PostForm()
    return save_formm(request, form, 'Atom/CRUD/create.html')

def aboutWall2(request, pk):
    model=Wall.objects.get(id=pk)
    mm = Post.objects.filter(Wall_id=pk).order_by('-publication_date')
    context={}
    context['object']=model
    context['posts']=mm
    return render_to_response(request,'Atom/wall_detail.html',context)


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  person=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.vote.create(person=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.vote.likes().count(),
                "dislike_count": obj.vote.dislikes().count(),
                "sum_rating": obj.vote.sum_rating()
            }),
            content_type="application/json"
        )

from social_django.models import UserSocialAuth

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'Joe/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


def tryy(request):
    return render(request, "Atom/static/Try.html")

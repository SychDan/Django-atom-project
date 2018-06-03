from . import views,form,serialize, models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls import include, url
from rest_framework import routers

app_name = 'Atom'

router = routers.DefaultRouter()
router.register(r'users', serialize.UserViewSet)

urlpatterns = [
    url(r'^json/', include(router.urls)),
    url(r'^search_wall/$', views.search_wall, name='search_wall'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', views.out, name='logout'),
    url(r'^$',views.init, name='init'),
    url(r'^start/$',views.start,name='start'),
    url(r'^comments/', views.LoadComments.as_view(), name="comm_list"),
    url(r'^posts/', views.LoadPosts.as_view(), name="page"),
    url(r'^post/(?P<pk>\d+)/$', views.aboutPosts.as_view(), name='post-detail'),
    url(r'^wall/(?P<pk>\d+)/$', views.aboutWalls.as_view(),name='wall-detail'),
    url(r'^wall2/(?P<pk>\d+)/$',views.aboutWall2,name='wall-detail2'),
    url(r'^person/(?P<pk>\d+)$',views.aboutPerson.as_view(),name='person-detail'),
    url(r'^search_user/$', views.indexxx, name='search_user'),
    url(r'^search_theme/$', views.search_theme, name='search_theme'),
    url(r'^search_post/$', views.search_post, name='search_post'),
    url(r'^login/$', views.ELoginView.as_view(), name='login'),
    url(r'^auth/$',views.simpleRegistration, name='auth'),
    url(r'^validate/$',views.validateUsername,name='validate'),
    url(r'^welcome/$',views.welcome, name='welcome'),
    url(r'^add_post/$',views.createPost, name='add-post'),
    url(r'^theme/(?P<pk>\d+)/$',views.aboutTheme.as_view(),name='theme-detail'),
    url(r'^h/$',views.post_list,name='post_list'),
    url(r'^dd/$',views.indexx, name='dd'),
    url(r'^dd/more/$',views.dd,name="more"),
    url(r'^new/$',views.newbase,name='new'),
    url(r'^rest/$',views.rest,name='rest'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^faq/$',views.faq,name='faq'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.delete, name='delete'),
    url(r'^post/(?P<pk>\d+)/update/$',views.update,name='update'),
    url(r'^post/create/$',views.create,name='create'),
    url(r'^post/create/Wall/$',views.createm,name='createm'),
    url(r'^newbase/$',views.newbase,name='newbase'),
    url(r'^post/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=models.Post, vote_type=models.LikeDislike.LIKE)),
        name='article_like'),
    url(r'^post/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=models.Post, vote_type=models.LikeDislike.DISLIKE)),
        name='article_dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=models.Comment, vote_type=models.LikeDislike.LIKE)),
        name='comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=models.Comment, vote_type=models.LikeDislike.DISLIKE)),
        name='comment_dislike'),
    url(r'^tryy/$',views.tryy,name='tryy'),
    ]

urlpatterns+=[
]
if settings.DEBUG:
   import debug_toolbar
   urlpatterns += [
       url(r'^__debug__/', include(debug_toolbar.urls)),
   ]
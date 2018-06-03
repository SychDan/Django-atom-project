from django.contrib.auth.models import User
import django_filters
from .models import Wall,Post, Person
from django.contrib.auth import get_user_model

class UserFilter(django_filters.FilterSet):
    username=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = get_user_model()

        fields = ['username' ]


class PostFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Post

        fields = ['title' ]

class WallFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Wall

        fields = ['name' ]


from django.contrib import admin

from .models import Person
from .models import Post
from .models import Theme
from .models import Wall
from .models import Comment
from .models import State
from .models import Place
from .models import LikeDislike

class WallAdmin(admin.ModelAdmin):
    raw_id_fields = ('place',)
    pass
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('person','Wall',)
    pass
class PlaceAdmin(admin.ModelAdmin):
    raw_id_fields = ('state',)
    pass
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('post','person')
    pass
class ThemeAdmin(admin.ModelAdmin):
    raw_id_fields = ('post',)
    pass
admin.site.register(Person)
admin.site.register(Post, PostAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Wall, WallAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(State)
admin.site.register(Place, PlaceAdmin)
admin.site.register(LikeDislike)


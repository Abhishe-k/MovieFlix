from django.contrib import admin
from .models import actor, movie, topmovie, profile, order, usertoken, userlikes, Comment, Contact, MovieOrder

# Register your models here.

admin.site.register(actor)
admin.site.register(movie)
admin.site.register(topmovie)
admin.site.register(profile)
admin.site.register(order)
admin.site.register(userlikes)
admin.site.register(Contact)
admin.site.register(MovieOrder)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'body', 'created_on', 'active')
    actions = ['disable_comments', 'approve_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(usertoken)
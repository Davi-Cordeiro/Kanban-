from django.contrib import admin
from boards.models import BoardInfo, LabelInfo, ListInfo, CardInfo

@admin.register(BoardInfo)
class BoardInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at',)
    search_fields = ('title', 'owner__username',)

@admin.register(LabelInfo)
class LabelInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'board')
    search_fields = ('name', 'board__title',)

@admin.register(ListInfo)
class ListInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'board')
    search_fields = ('title', 'board__title',)
    ordering = ('board', 'position',)

@admin.register(CardInfo)
class CardInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'assignee', 'deadline')
    search_fields = ('title', 'list__title', 'assignee__username', 'labels__name',)
    list_filter = ('deadline', 'labels',)
    ordering = ('list', 'position',)

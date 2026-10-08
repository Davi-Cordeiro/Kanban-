from django.contrib import admin
from boards.models import BoardInfo, LabelInfo, ListInfo, CardInfo

@admin.register(BoardInfo)
class BoardInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at',)
    search_fields = ('title', 'owner__username',)
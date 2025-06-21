# pages/admin.py

from django.contrib import admin
from .models import StaticPage

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    # Preenche o campo 'slug' automaticamente a partir do 'title'
    # enquanto você digita. Uma grande ajuda para os redatores!
    prepopulated_fields = {'slug': ('title',)}
from django.contrib import admin

from . import models

# Register your models here.

class WordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'word', 'pinyin', 'translation']
    list_editable = ['word', 'pinyin', 'translation']

admin.site.register(models.Words, WordAdmin)
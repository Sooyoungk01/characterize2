from django.contrib import admin
from .models import Characters

# Register your models here.


@admin.register(Characters)
class CharacterModel(admin.ModelAdmin):
    list_filter = ('name', 'id_ch')


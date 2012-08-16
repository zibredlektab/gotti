from cards.models import Card
from django.contrib import admin

class CardAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'first', 'died']

admin.site.register(Card, CardAdmin)

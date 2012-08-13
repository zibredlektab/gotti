from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'cards.views.home', name='home'),
    url(r'^settings', 'cards.views.settings', name='settings'),
    url(r'(?P<slug>.*)', 'cards.views.show_card', name='show_card'),
)

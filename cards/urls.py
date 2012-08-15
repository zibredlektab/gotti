from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'cards.views.home', name='home'),
    url(r'^settings$', 'cards.views.settings', name='settings'),
    url(r'^export$', 'cards.views.export_all'),
    url(r'^import$', 'cards.views.import_lots'),
    url(r'^(?P<slug>\w+)$', 'cards.views.show_card', name='show_card'),
    url(r'^(?P<slug>\w+)/export$', 'cards.views.yaml_card'),
)

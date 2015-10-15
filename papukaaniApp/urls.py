from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /papukaani/
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    # ex: /papukaani/public/1/
    url(r'^public/(?P<creature_id>[0-9]+)/$', views.public, name='public'),
    # ex: /papukaani/creature/1/
    url(r'^creature/(?P<creature_id>[0-9]+)/$', views.creature, name='creature'),
    # ex: /papukaani/creatures/
    url(r'^creatures/$', views.creatures, name='creatures'),
    url(r'^choose/$', views.choose, name='choose')
]

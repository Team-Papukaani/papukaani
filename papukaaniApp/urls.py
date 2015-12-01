from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /papukaani/
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    # ex: /papukaani/public/1/
    url(r'^public/$', views.public, name='public'),
    # ex: /papukaani/creature/1/
    url(r'^creature/(?P<creature_id>[0-9]+)/$', views.creature, name='creature'),
    # ex: /papukaani/creatures/
    url(r'^creatures/$', views.creatures, name='creatures'),
    url(r'^choose/$', views.choose, name='choose'),
    # ex: /papukaani/devices/
    url(r'^devices/$', views.devices, name='devices'),
    url(r'^devices/(?P<device_id>.+)/attach/$', views.attach_to),
    url(r'^devices/(?P<device_id>.+)/remove/$', views.remove_from),
    # ex: /papukaani/individuals/
    url(r'^individuals/$', views.individuals, name='individuals'),
    url(r'^rest/documentsForDevice$', views.getDocumentsForDevice),
    url(r'^rest/documentsForIndividual$', views.getDocumentsForIndividual),

    url(r'^formats/$', views.formats, name='formats')
]

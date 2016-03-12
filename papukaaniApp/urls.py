from django.conf.urls import url

from papukaaniApp import views

urlpatterns = [
    # ex: /papukaani/
    url(r'^$', views.index, name='index'),
    url(r'^choose/$', views.choose, name='choose'),
    url(r'^devices/$', views.devices, name='devices'),
    url(r'^devices/(?P<device_id>.+)/attach/$', views.attach_to),
    url(r'^devices/(?P<device_id>.+)/remove/$', views.remove_from),
    url(r'^formats/create/(?P<id>.+)/$', views.show_format, name='create_format'),
    url(r'^formats/$', views.list_formats, name='list_formats'),
    url(r'^formats/(?P<id>.+)/$', views.show_format, name="show_format"),
    url(r'^formats/(?P<id>.+)/delete$', views.delete_format, name="delete_format"),
    url(r'^individuals/$', views.individuals, name='individuals'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^news/$', views.news, name='news'),
    url(r'^public/$', views.public, name='public'),
    url(r'^rest/gatheringsForDevice$', views.getGatheringsForDevice),
    url(r'^rest/gatheringsForIndividual$', views.getGatheringsForIndividual),
    url(r'^upload/$', views.upload, name='upload')
]

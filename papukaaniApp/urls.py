from django.conf.urls import url

from papukaaniApp import views

urlpatterns = [
    # ex: /papukaani/
    url(r'^$', views.index, name='index'),
    url(r'^choose/$', views.choose, name='choose'),
    url(r'^choose/setIndividualGatherings$', views.set_individual_gatherings),

    url(r'^devices/$', views.devices, name='devices'),
    url(r'^devices/attachments/(?P<attachment_id>.+)$', views.attachments_rest),
    url(r'^devices/attachments/$', views.attachments_rest_root),

    url(r'^formats/create/(?P<id>.+)/$', views.show_format, name='create_format'),
    url(r'^formats/$', views.list_formats, name='list_formats'),
    url(r'^formats/(?P<id>.+)/$', views.show_format, name="show_format"),
    url(r'^formats/(?P<id>.+)/delete$', views.delete_format, name="delete_format"),
    url(r'^individuals/$', views.individuals, name='individuals'),
    url(r'^rest/gatheringsForDevice$', views.getGatheringsForDevice),
    url(r'^rest/gatheringsForIndividual$', views.getPublicGatheringsForIndividual),
    url(r'^rest/allGatheringsForIndividual$', views.getAllGatheringsForIndividual),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^news/$', views.news_index, name='news'),
    url(r'^news/list$', views.news_list, name='news_list'),
    url(r'^news/(\d+)$', views.news_rest, name='news_rest'),
    url(r'^public/$', views.public, name='public'),
    url(r'^upload/$', views.upload, name='upload')
]

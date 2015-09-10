from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^public/', views.public),
    url(r'^upload/', views.upload)
]

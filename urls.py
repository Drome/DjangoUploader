from django.conf.urls import url

from uploader import views

urlpatterns = [
    url(r'^$', views.index, name='uploader-index'),
    url(r'^thanks/', views.thanks, name='uploader-thanks'),
    url(r'^uploads/(.*)', views.uploads, name='uploader-uploads'),
]

from django.conf.urls import include, url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^stream/(?P<user_id>[0-9]+)/$', views.stream, name='stream'),
    url(r'^post/$', views.post, name='post'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),

    # The External Service sends POST data to this URL to add a hashtag.
    # TODO: possibly remove this URL and have views.hashtag add new tags automatically,
    #       which could simplify what the external service must check for
    url(r'^hashtag/add/$', views.add_hashtag, name='add_hashtag'),

    # Use this URL to display posts with a given hashtag
    url(r'^hashtag/(?P<view_tag>[\w\-]+)/$', views.hashtag, name='hashtag_stream'),

    # The External Service sends POST data to this URL to tag a post.
    url(r'^post/tag/$', views.tag_post, name='tag_post'),

    url(r'^follow/$', views.follow, name='follow'),
    url(r'^register/$', views.register, name='register'),
    url('^', include('django.contrib.auth.urls'))
]

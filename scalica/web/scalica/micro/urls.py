from django.conf.urls import include, url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^stream/(?P<user_id>[0-9]+)/$', views.stream, name='stream'),
    url(r'^post/$', views.post, name='post'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),

    # Use this URL to display posts with a given hashtag
    # TODO: check the regex for this. Hashtags use a CharField, which will be the slug.
    #url(r'^hashtag/(?P<hashtag>[A-Z]+)/$', views.hashtag, name='hashtag_stream'),

    # The External Service sends POST data to this URL to add a hashtag.
    #url(r'^hashtag/add/$', views.add_hashtag, name='add_hashtag'),

    # The External Service sends POST data to this URL to tag a post.
    #url(r'^post/tag/$', views.tag_post, name='tag_post'),

    url(r'^follow/$', views.follow, name='follow'),
    url(r'^register/$', views.register, name='register'),
    url('^', include('django.contrib.auth.urls'))
]

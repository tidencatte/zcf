from django.conf.urls.defaults import *

urlpatterns = patterns('naz.forum.views',
    url("forum/([0-9]+)/$", "view_forum", name="view_forum"),
    url("thread/([0-9]+).([0-9]+)/$", "view_thread", name="view_thread"),
    url("newreply/([0-9]+)/$", "new_reply", name="new_reply"),
    url("$", 'index'),
)

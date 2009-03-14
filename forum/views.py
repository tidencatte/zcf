# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from naz.forum.models import Forum, Category, Thread, Post, PostRevision, Profile
from naz.forum.forms  import PostForm

def index(request):
    return render_to_response("forum/default/index.html",
            {"categories": Category.objects.select_related().order_by("-z_index")},RequestContext(request))

def view_forum(request, forum_id):
    threads  = Thread.objects.filter(forum__id__exact=forum_id).select_related()[0:20]
    forum    = Forum.objects.select_related().get(pk=forum_id)
    return render_to_response("forum/default/forum_list.html",
            {"forum": forum, "threads": threads}, RequestContext(request))

def view_thread(request, thread_id, page_offset=0):
    posts    = Post.objects\
            .filter(thread__id__exact=thread_id)\
            .select_related()[0:20]

    thread   = Thread.objects\
            .select_related()\
            .get(pk=thread_id)

    forum    = Forum.objects\
            .get(pk=thread.forum_id)
    context  = RequestContext(
            request,
            {"forum": forum,
             "thread": thread,
             "posts": posts})

    template = get_template("forum/default/thread_list.html")
    try:
        return HttpResponse(template.render(context))
    finally:
        thread.views += 1
        thread.save()

def profile(request, profile_id):
    profile = Profile.objects.select_related().get(pk=1)
    return render_to_response(
            "forum/default/profile.html",
            {"profile": profile}, RequestContext(request))


@login_required
def new_reply(request, threadid):
    thread   = Thread.objects.get(pk=threadid)
    form     = PostForm(request.POST)
    posts    = Post.objects\
            .filter(thread__id__exact=threadid)\
            .order_by("-posted")[:15]\
            .select_related()
    context  = RequestContext(request,
            {"thread": thread, "form": form, "posts": posts, "errors": None})
    template = get_template("forum/default/newreply.html")
    prof = request.user.get_profile()
    if form.is_valid() and request.method == "POST":
        fields = filter(lambda x: x != "post_content", form.cleaned_data)
        fields = map(lambda x: (x,form.cleaned_data[x]), fields)
        fields.append(("user", request.user))
        fields.append(("thread", thread))
        p  = Post(**dict(fields))
        p.save()
        pr = PostRevision(
                ip=request.META["REMOTE_ADDR"],
                content=form.cleaned_data["post_content"],
                post=p)
        pr.save()
        prof.posts += 1
        prof.save()
        thread.replies += 1
        thread.save()
        return HttpResponseRedirect(
                reverse(
                    "view_thread",
                    args=[thread.id, int(round(thread.replies/20))]))

    return HttpResponse(template.render(context))

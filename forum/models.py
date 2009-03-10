from django.db import models
from django.contrib.auth.models import User,Group

class Profile(models.Model):
    # CHOICE TYPES
    OPT_SIG_SEP_TYPES = (
            (0,"None"),
            (1,"Horizontal Rule <hr>"),
            (2,"Dashes"),
            (3,"Em Dashes"))

    OPT_SEX_TYPES = (
            (0, "N/A"),
            (1, "Male"),
            (2, "Female"),
            (3, "~MYSTERIOUS FOURTH OPTION~"))

    user             = models.ForeignKey(User, unique=True)
    posts            = models.IntegerField(default=0, blank=False) # intentional.
    threads          = models.PositiveIntegerField()
    last_ip          = models.IPAddressField()
    last_url         = models.CharField(max_length=255)
    last_post_time   = models.DateTimeField(auto_now_add=True)
    last_view_time   = models.DateTimeField(auto_now_add=True)
    signature        = models.TextField(blank=True, default="")
    sex              = models.SmallIntegerField(choices=OPT_SEX_TYPES, default=0)

    user_image       = models.URLField(blank=True, null=True, default=None)

    # option flags
    option_enable_signatures = models.BooleanField(default=True)
    option_threads_per_page  = models.SmallIntegerField(default=30)
    option_posts_per_page    = models.SmallIntegerField(default=30)
    option_hide_email        = models.BooleanField(default=True)

    option_sig_separator     = models.SmallIntegerField(choices=OPT_SEX_TYPES, default=1)

class Category(models.Model):
    groups_whitelist = models.ManyToManyField(Group, null=True, blank=True)
    title            = models.CharField(max_length=130)
    min_power        = models.IntegerField(default=0)
    max_power        = models.IntegerField(null=True, blank=True)
    z_index          = models.PositiveIntegerField()
    is_hidden        = models.BooleanField(default=False)

class Forum(models.Model):
    category         = models.ForeignKey(Category)
    title            = models.CharField(max_length=130)
    description      = models.CharField(max_length=400)
    local_moderators = models.ManyToManyField(User, blank=True, null=True)
    z_index          = models.PositiveIntegerField()
    post_count       = models.PositiveIntegerField()
    thread_count     = models.PositiveIntegerField()
    last_post        = models.ForeignKey("Post", blank=True, null=True)
    min_power        = models.IntegerField()
    min_power_reply  = models.IntegerField()
    max_power        = models.IntegerField(null=True, blank=True)
    max_power_reply  = models.IntegerField(null=True, blank=True)

    is_hidden        = models.BooleanField(default=False, blank=True)
    is_locked        = models.BooleanField(default=False, blank=True)

class Thread(models.Model):
    user             = models.ForeignKey(User)
    forum            = models.ForeignKey(Forum)
    title            = models.CharField(max_length=150)
    replies          = models.PositiveIntegerField()
    views            = models.PositiveIntegerField()
    last_reply       = models.ForeignKey("Post", related_name="thread_last")
    is_locked        = models.BooleanField(default=False, blank=True)
    is_trashed       = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return "%s" % self.title

class Post(models.Model):
    user             = models.ForeignKey(User)
    thread           = models.ForeignKey(Thread)
    posted           = models.DateTimeField(auto_now_add=True, auto_now=True)
    is_disemvoweled  = models.BooleanField(default=False, blank=True)
    is_deleted       = models.BooleanField(default=False, blank=True)
    is_hamtardized   = models.BooleanField(default=False, blank=True)
    smilies_disabled = models.BooleanField(default=False, blank=True)
    markup_disabled  = models.BooleanField(default=False, blank=True)
    html_disabled    = models.BooleanField(default=False, blank=True)

class PostRevision(models.Model):
    post       = models.ForeignKey(Post, related_name="revisions")
    content    = models.TextField()
    ip         = models.IPAddressField()
    rtime      = models.DateTimeField("Revision Time", auto_now_add=True)

    class Meta:
        get_latest_by = "rtime"

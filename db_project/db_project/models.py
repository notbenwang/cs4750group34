# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appuser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    biography = models.TextField(blank=True, null=True)
    is_database_admin = models.BooleanField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    karma = models.IntegerField(blank=True, null=True)
    auth = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appuser'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Posts', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Appuser, models.DO_NOTHING, blank=True, null=True)
    reply_to_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField()
    creation_date = models.DateTimeField(blank=True, null=True)
    upvotes = models.IntegerField(blank=True, null=True)
    downvotes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class CommentInteraction(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'comment_id')
    user = models.ForeignKey(Appuser, models.DO_NOTHING)
    comment = models.ForeignKey(Comment, models.DO_NOTHING)
    interaction_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_interaction'
        unique_together = (('user', 'comment'),)


class Community(models.Model):
    community_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    about = models.TextField(blank=True, null=True)
    member_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'community'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PostInteraction(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'

    INTERACTION_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    pk = models.CompositePrimaryKey('user_id', 'post_id')
    user = models.ForeignKey(Appuser, models.DO_NOTHING)
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_interaction'
        unique_together = (('user', 'post'),)


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Appuser, models.DO_NOTHING, blank=True, null=True)
    community = models.ForeignKey(Community, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    creation_date = models.DateTimeField(blank=True, null=True)
    upvotes = models.IntegerField(blank=True, null=True)
    downvotes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class Usercommunity(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'community_id')
    user = models.ForeignKey(Appuser, models.DO_NOTHING)
    community = models.ForeignKey(Community, models.DO_NOTHING)
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usercommunity'
        unique_together = (('user', 'community'),)

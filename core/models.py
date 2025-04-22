from django.db import models

# These are not actual Django ORM models, just helper classes to represent database entities
# We won't use them for direct database operations, just to help with form validation and business logic

class User:
    def __init__(self, user_id=None, username=None, email=None, bio=None, created_at=None, is_admin=False, **kwargs):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.bio = bio
        self.created_at = created_at
        self.is_admin = is_admin

class Group:
    def __init__(self, group_id=None, name=None, description=None, group_type=None, created_at=None, created_by=None, **kwargs):
        self.group_id = group_id
        self.name = name
        self.description = description
        self.group_type = group_type
        self.created_at = created_at
        self.created_by = created_by

class Post:
    def __init__(self, post_id=None, group_id=None, user_id=None, title=None, content=None, created_at=None, updated_at=None, **kwargs):
        self.post_id = post_id
        self.group_id = group_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

class Comment:
    def __init__(self, comment_id=None, post_id=None, user_id=None, parent_comment_id=None, content=None, created_at=None, updated_at=None, **kwargs):
        self.comment_id = comment_id
        self.post_id = post_id
        self.user_id = user_id
        self.parent_comment_id = parent_comment_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

class Notification:
    def __init__(self, notification_id=None, user_id=None, triggered_by=None, notification_type=None, reference_id=None, content=None, created_at=None, is_read=False, **kwargs):
        self.notification_id = notification_id
        self.user_id = user_id
        self.triggered_by = triggered_by
        self.notification_type = notification_type
        self.reference_id = reference_id
        self.content = content
        self.created_at = created_at
        self.is_read = is_read
import psycopg2
from psycopg2 import extras
from django.conf import settings
from django.db import connection


# Base functions to call PostgreSQL stored procedures
def execute_function(function_name, params=None):
    """Execute a PostgreSQL function and return the result."""
    with connection.cursor() as cursor:
        if params:
            cursor.callproc(function_name, params)
        else:
            cursor.callproc(function_name)

        try:
            result = cursor.fetchall()
            return result
        except psycopg2.ProgrammingError:
            # No results to fetch
            return None


def execute_function_scalar(function_name, params=None):
    """Execute a PostgreSQL function and return a single scalar value."""
    with connection.cursor() as cursor:
        if params:
            cursor.callproc(function_name, params)
        else:
            cursor.callproc(function_name)

        result = cursor.fetchone()
        return result[0] if result else None


def execute_function_returning_table(function_name, params=None):
    """Execute a PostgreSQL function that returns a table."""
    with connection.cursor(cursor_factory=extras.DictCursor) as cursor:
        if params:
            cursor.callproc(function_name, params)
        else:
            cursor.callproc(function_name)

        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        return []


# User functions
def register_user(username, email, password, bio=""):
    """Register a new user."""
    return execute_function_scalar("register_user", [username, email, password, bio])


def authenticate_user(username, password):
    """Authenticate a user."""
    result = execute_function_returning_table("authenticate_user", [username, password])
    return result[0] if result else None


def update_user_profile(user_id, bio):
    """Update user profile."""
    return execute_function_scalar("update_user_profile", [user_id, bio])


# Group functions
def create_group(name, description, group_type, created_by):
    """Create a new group."""
    return execute_function_scalar("create_group", [name, description, group_type, created_by])


def join_group(group_id, user_id):
    """Join a group."""
    return execute_function_scalar("join_group", [group_id, user_id])


def leave_group(group_id, user_id):
    """Leave a group."""
    return execute_function_scalar("leave_group", [group_id, user_id])


def approve_join_request(request_id, approved_by):
    """Approve a join request."""
    return execute_function_scalar("approve_join_request", [request_id, approved_by])


def change_group_privacy(group_id, new_type, changed_by):
    """Change group privacy."""
    return execute_function_scalar("change_group_privacy", [group_id, new_type, changed_by])


def appoint_moderator(group_id, user_id, appointed_by):
    """Appoint a moderator."""
    return execute_function_scalar("appoint_moderator", [group_id, user_id, appointed_by])


def remove_moderator(group_id, user_id, removed_by):
    """Remove a moderator."""
    return execute_function_scalar("remove_moderator", [group_id, user_id, removed_by])


def transfer_admin(group_id, new_admin_id, current_admin_id):
    """Transfer admin status."""
    return execute_function_scalar("transfer_admin", [group_id, new_admin_id, current_admin_id])


def delete_group(group_id, user_id):
    """Delete a group."""
    return execute_function_scalar("delete_group", [group_id, user_id])


# Post functions
def create_post(group_id, user_id, title, content):
    """Create a post."""
    return execute_function_scalar("create_post", [group_id, user_id, title, content])


def delete_post(post_id, deleted_by):
    """Delete a post."""
    return execute_function_scalar("delete_post", [post_id, deleted_by])


def edit_post(post_id, user_id, title, content):
    """Edit a post."""
    return execute_function_scalar("edit_post", [post_id, user_id, title, content])


def vote_on_post(post_id, user_id, vote_value):
    """Vote on a post."""
    return execute_function_scalar("vote_on_post", [post_id, user_id, vote_value])


def save_post(post_id, user_id):
    """Save a post."""
    return execute_function_scalar("save_post", [post_id, user_id])


def unsave_post(post_id, user_id):
    """Unsave a post."""
    return execute_function_scalar("unsave_post", [post_id, user_id])


def get_saved_posts(user_id):
    """Get saved posts."""
    return execute_function_returning_table("get_saved_posts", [user_id])


# Comment functions
def create_comment(post_id, user_id, content, parent_comment_id=None):
    """Create a comment."""
    return execute_function_scalar("create_comment", [post_id, user_id, content, parent_comment_id])


def delete_comment(comment_id, deleted_by):
    """Delete a comment."""
    return execute_function_scalar("delete_comment", [comment_id, deleted_by])


def edit_comment(comment_id, user_id, content):
    """Edit a comment."""
    return execute_function_scalar("edit_comment", [comment_id, user_id, content])


def vote_on_comment(comment_id, user_id, vote_value):
    """Vote on a comment."""
    return execute_function_scalar("vote_on_comment", [comment_id, user_id, vote_value])


# Moderation functions
def ban_user_from_group(group_id, user_id, banned_by, reason=""):
    """Ban a user from a group."""
    return execute_function_scalar("ban_user_from_group", [group_id, user_id, banned_by, reason])


def unban_user_from_group(group_id, user_id, unbanned_by, reason=""):
    """Unban a user from a group."""
    return execute_function_scalar("unban_user_from_group", [group_id, user_id, unbanned_by, reason])


# Notification functions
def mark_notification_read(notification_id, user_id):
    """Mark notification as read."""
    return execute_function_scalar("mark_notification_read", [notification_id, user_id])


def get_unread_notifications(user_id):
    """Get unread notifications."""
    return execute_function_returning_table("get_unread_notifications", [user_id])


# View data access functions
def get_all_groups():
    """Get all groups."""
    # Use callable to query the v_group_details view
    return execute_function_returning_table("get_all_groups")


def search_groups(search_term):
    """Search groups."""
    return execute_function_returning_table("search_groups", [search_term])


def get_group_details(group_id):
    """Get group details."""
    results = execute_function_returning_table("get_group_details", [group_id])
    return results[0] if results else None


def get_group_moderators(group_id):
    """Get group moderators."""
    return execute_function_returning_table("get_group_moderators", [group_id])


def get_group_posts(group_id, sort_by_top=False):
    """Get group posts."""
    if sort_by_top:
        return execute_function_returning_table("get_group_top_posts", [group_id])
    else:
        # Call the regular group posts function
        return execute_function_returning_table("get_group_posts", [group_id])


def get_post_with_comments(post_id):
    """Get post with comments."""
    return execute_function_returning_table("get_post_with_comments", [post_id])


def get_user_profile(user_id):
    """Get user profile."""
    results = execute_function_returning_table("get_user_profile", [user_id])
    return results[0] if results else None


def get_user_content(user_id, sort_by_top=False):
    """Get user content."""
    if sort_by_top:
        return execute_function_returning_table("get_user_top_content", [user_id])
    else:
        # Call the regular user content function
        return execute_function_returning_table("get_user_content", [user_id])


def get_user_feed(user_id):
    """Get user feed."""
    return execute_function_returning_table("get_user_feed", [user_id])


def can_access_group(group_id, user_id):
    """Check if user can access group."""
    return execute_function_scalar("can_access_group", [group_id, user_id])


def is_banned_from_group(group_id, user_id):
    """Check if user is banned from group."""
    return execute_function_scalar("is_banned_from_group", [group_id, user_id])


def get_user_role_in_group(group_id, user_id):
    """Get user role in group."""
    return execute_function_scalar("get_user_role_in_group", [group_id, user_id])


def get_group_join_requests(group_id):
    """Get group join requests."""
    return execute_function_returning_table("get_group_join_requests", [group_id])


def get_group_banned_users(group_id):
    """Get banned users from a group."""
    return execute_function_returning_table("get_group_banned_users", [group_id])


def get_group_members(group_id):
    """Get group members."""
    return execute_function_returning_table("get_group_members", [group_id])


def get_user_by_id(user_id):
    """Get user by ID."""
    results = execute_function_returning_table("get_user_by_id", [user_id])
    return results[0] if results else None


def get_user_by_username(username):
    """Get user by username."""
    results = execute_function_returning_table("get_user_by_username", [username])
    return results[0] if results else None
from django.urls import path
from . import views

urlpatterns = [
    # Main routes
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('editmybio/', views.edit_bio, name='edit_bio'),
    path('search/', views.search_groups_view, name='search_groups'),

    # Group routes
    path('create_group/', views.create_group_view, name='create_group'),
    path('group/<str:group_name>/', views.group_detail, name='group_detail'),
    path('group/<str:group_name>/create_post/', views.create_post_view, name='create_post'),
    path('group/<str:group_name>/approve_joins/', views.approve_joins, name='approve_joins'),
    path('group/<str:group_name>/ban/', views.ban_user, name='ban_user'),
    path('group/<str:group_name>/unban/', views.unban_user, name='unban_user'),
    path('group/<str:group_name>/appoint_moderator/', views.appoint_moderator_view, name='appoint_moderator'),
    path('group/<str:group_name>/step_down/', views.step_down, name='step_down'),

    # Post routes
    path('group/<str:group_name>/<int:post_id>/', views.post_detail, name='post_detail'),
    path('vote_post/<int:post_id>/<str:vote_type>/', views.vote_post, name='vote_post'),
    path('delete_post/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('edit_post/<int:post_id>/', views.edit_post_view, name='edit_post'),
    path('save_post/<int:post_id>/', views.save_post_view, name='save_post'),
    path('unsave_post/<int:post_id>/', views.unsave_post_view, name='unsave_post'),

    # Comment routes
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment_view, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('vote_comment/<int:comment_id>/<str:vote_type>/', views.vote_comment, name='vote_comment'),

    # Group membership routes
    path('join_group/<int:group_id>/', views.join_group_view, name='join_group'),
    path('leave_group/<int:group_id>/', views.leave_group_view, name='leave_group'),

    # User routes
    path('user/<str:username>/', views.user_profile, name='user_profile'),

    # Notification routes
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read_view,
         name='mark_notification_read'),

    # Top content routes
    path('group/<str:group_name>/top/', views.group_top_posts, name='group_top_posts'),
    path('user/<str:username>/top/', views.user_top_content, name='user_top_content'),
]
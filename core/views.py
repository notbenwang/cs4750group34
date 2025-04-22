@login_required
def edit_post_view(request, post_id):
    """Edit a post."""
    user = get_current_user(request)

    # Get post info
    post_data = db.fetch_all_from_query("""
        SELECT p.post_id, p.user_id, p.group_id, g.name, p.title, p.content 
        FROM posts p 
        JOIN groups g ON p.group_id = g.group_id 
        WHERE p.post_id = %s AND p.is_deleted = FALSE
    """, [post_id])

    if not post_data:
        messages.error(request, "Post not found.")
        return redirect('home')

    post = post_data[0]

    # Check if user is author
    if post['user_id'] != user['user_id']:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('post_detail', group_name=post['name'], post_id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Edit post
            success = db.edit_post(
                post_id,
                user['user_id'],
                form.cleaned_data['title'],
                form.cleaned_data['content']
            )

            if success:
                messages.success(request, "Post edited successfully.")
                return redirect('post_detail', group_name=post['name'], post_id=post_id)
            else:
                messages.error(request, "Failed to edit post.")
    else:
        form = PostForm(initial={
            'title': post['title'],
            'content': post['content']
        })

    return render(request, 'post/create.html', {
        'form': form,
        'user': user,
        'edit_mode': True,
        'group_name': post['name'],
        'notifications': get_notifications(request)
    })


@login_required
def save_post_view(request, post_id):
    """Save a post."""
    user = get_current_user(request)

    # Get post info
    post_data = db.fetch_all_from_query("""
        SELECT p.post_id, g.name 
        FROM posts p 
        JOIN groups g ON p.group_id = g.group_id 
        WHERE p.post_id = %s
    """, [post_id])

    if not post_data:
        messages.error(request, "Post not found.")
        return redirect('home')

    post = post_data[0]

    # Save post
    success = db.save_post(post_id, user['user_id'])

    if success:
        messages.success(request, "Post saved successfully.")
    else:
        messages.error(request, "Failed to save post.")

    return redirect('post_detail', group_name=post['name'], post_id=post_id)


@login_required
def unsave_post_view(request, post_id):
    """Unsave a post."""
    user = get_current_user(request)

    # Get post info
    post_data = db.fetch_all_from_query("""
        SELECT p.post_id, g.name 
        FROM posts p 
        JOIN groups g ON p.group_id = g.group_id 
        WHERE p.post_id = %s
    """, [post_id])

    if not post_data:
        messages.error(request, "Post not found.")
        return redirect('home')

    post = post_data[0]

    # Unsave post
    success = db.unsave_post(post_id, user['user_id'])

    if success:
        messages.success(request, "Post unsaved successfully.")
    else:
        messages.error(request, "Failed to unsave post.")

    return redirect('post_detail', group_name=post['name'], post_id=post_id)


@login_required
def delete_comment_view(request, comment_id):
    """Delete a comment."""
    user = get_current_user(request)

    # Get comment info
    comment_data = db.fetch_all_from_query("""
        SELECT c.comment_id, c.user_id, c.post_id, p.group_id, g.name 
        FROM comments c 
        JOIN posts p ON c.post_id = p.post_id 
        JOIN groups g ON p.group_id = g.group_id 
        WHERE c.comment_id = %s
    """, [comment_id])

    if not comment_data:
        messages.error(request, "Comment not found.")
        return redirect('home')

    comment = comment_data[0]

    # Check if user is author or moderator/admin
    is_author = comment['user_id'] == user['user_id']
    role = db.get_user_role_in_group(comment['group_id'], user['user_id'])

    if not is_author and not role in ['moderator', 'admin']:
        messages.error(request, "You do not have permission to delete this comment.")
        return redirect('post_detail', group_name=comment['name'], post_id=comment['post_id'])

    # Delete comment
    success = db.delete_comment(comment_id, user['user_id'])

    if success:
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "Failed to delete comment.")

    return redirect('post_detail', group_name=comment['name'], post_id=comment['post_id'])


@login_required
def edit_comment_view(request, comment_id):
    """Edit a comment."""
    user = get_current_user(request)

    # Get comment info
    comment_data = db.fetch_all_from_query("""
        SELECT c.comment_id, c.user_id, c.post_id, c.content, p.group_id, g.name 
        FROM comments c 
        JOIN posts p ON c.post_id = p.post_id 
        JOIN groups g ON p.group_id = g.group_id 
        WHERE c.comment_id = %s AND c.is_deleted = FALSE
    """, [comment_id])

    if not comment_data:
        messages.error(request, "Comment not found.")
        return redirect('home')

    comment = comment_data[0]

    # Check if user is author
    if comment['user_id'] != user['user_id']:
        messages.error(request, "You do not have permission to edit this comment.")
        return redirect('post_detail', group_name=comment['name'], post_id=comment['post_id'])

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Edit comment
            success = db.edit_comment(
                comment_id,
                user['user_id'],
                form.cleaned_data['content']
            )

            if success:
                messages.success(request, "Comment edited successfully.")
            else:
                messages.error(request, "Failed to edit comment.")

            return redirect('post_detail', group_name=comment['name'], post_id=comment['post_id'])
    else:
        form = CommentForm(initial={'content': comment['content']})

    return render(request, 'post/edit_comment.html', {
        'form': form,
        'user': user,
        'comment': comment,
        'notifications': get_notifications(request)
    })


@login_required
def mark_notification_read_view(request, notification_id):
    """Mark notification as read."""
    user = get_current_user(request)

    # Mark notification as read
    success = db.mark_notification_read(notification_id, user['user_id'])

    if not success:
        messages.error(request, "Failed to mark notification as read.")

    # Redirect back to the previous page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('home')


# Helper function for getting notifications
def get_notifications(request):
    """Get notifications for the current user."""
    user_id = request.session.get('user_id')
    if not user_id:
        return []

    return db.get_unread_notifications(user_id)
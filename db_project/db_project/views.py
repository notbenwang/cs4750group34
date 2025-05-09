from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, F
from django.db.models import ExpressionWrapper, IntegerField
from django.db import IntegrityError
from .forms import ProfileEditForm, CreateCommunityForm, CommentCreateForm, CommentEditForm, PostEditForm
from .models import Community, Posts, Appuser, Usercommunity, PostInteraction, Comment, CommentInteraction
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from urllib.parse import quote
from django.shortcuts import (
    get_object_or_404, render, redirect
)
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


def moderator_required(view_func):
    def wrapper(request, community_name, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Login required")
        community = get_object_or_404(Community, name=community_name)
        try:
            role = (
                Usercommunity.objects
                .get(user__auth_id=request.user.id, community=community)
                .role
            )
            if role not in ("moderator", "admin"):
                return HttpResponseForbidden("Moderator privileges required")
        except Usercommunity.DoesNotExist:
            return HttpResponseForbidden("Join the community first")
        return view_func(request, community_name, *args, **kwargs)

    return wrapper



def get_user_id_from_auth_id(user_id):
    return Appuser.objects.get(auth_id=user_id).user_id


def community_list(request):
    if not request.user.is_authenticated:
        return redirect("home")
    communities = Community.objects.all().order_by('name')
    return render(request, 'communities/communities.html', {'communities': communities})


def create_community(request):
    if not request.user.is_authenticated:
        return redirect("home")
    new_community = Community()

    if request.method == "POST":
        name = request.POST.get('name')
        about = request.POST.get('about')
        new_community = Community(name=name, about=about, member_count=0)
        form = CreateCommunityForm(request.POST, instance=new_community)
        if form.is_valid():
            form.save()
            creator_role = Usercommunity(user_id=get_user_id_from_auth_id(request.user.id),
                                         community_id=new_community.community_id, role="Owner")
            creator_role.save()
            return redirect('community_home', community_name=name)
    else:
        form = CreateCommunityForm(instance=new_community)
    return render(request, 'communities/create_community.html', {'form': form})


def community_posts(request, community_name):
    if not request.user.is_authenticated:
        return redirect("home")

    community = get_object_or_404(Community, name=community_name)

    posts = Posts.objects.filter(community=community).order_by('-creation_date')

    return render(request, 'communities/community_home.html', {
        'community': community,
        'posts': posts
    })


def create_post(request, community_name):
    if not request.user.is_authenticated:
        return redirect("home")

    appuser_id = get_user_id_from_auth_id(request.user.id)
    appuser = get_object_or_404(Appuser, pk=appuser_id)
    community = get_object_or_404(Community, name=community_name)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        new_post = Posts(
            user=appuser,
            community=community,
            title=title,
            content=content,
            creation_date=timezone.now(),
            upvotes=0,
            downvotes=0
        )
        new_post.save()
        return redirect("community_home", community_name=community.name)

    return render(request, "posts/create_post.html", {"community": community})


def post_detail(request, community_name, post_id):
    community = get_object_or_404(Community, name=community_name)
    post = get_object_or_404(Posts, post_id=post_id, community=community)

    is_owner = False
    user_vote = None

    if request.user.is_authenticated:
        try:
            app_user = Appuser.objects.get(auth_id=request.user.id)

            if app_user.user_id == post.user_id:
                is_owner = True

            interaction = PostInteraction.objects.filter(user=app_user, post=post).first()
            if interaction:
                user_vote = interaction.interaction_type

        except Appuser.DoesNotExist:
            pass


    up = PostInteraction.objects.filter(post=post, interaction_type='upvote').count()
    dn = PostInteraction.objects.filter(post=post, interaction_type='downvote').count()
    post.score = up - dn

    comments = (
        Comment.objects
        .filter(post=post)
        .select_related("user")
        .prefetch_related("comment_set")
        .annotate(
            upvotes_count=Count(
                "commentinteraction",
                filter=Q(commentinteraction__interaction_type="upvote")
            ),
            downvotes_count=Count(
                "commentinteraction",
                filter=Q(commentinteraction__interaction_type="downvote")
            ),
        )
        .annotate(
            score=ExpressionWrapper(
                F("upvotes_count") - F("downvotes_count"),
                output_field=IntegerField(),
            )
        )
    )

    comment_dict = {comment.comment_id: comment for comment in comments}
    root_comments = []

    for comment in comments:
        if comment.reply_to_comment_id is None:
            root_comments.append(comment)
        else:
            parent = comment_dict.get(comment.reply_to_comment_id)
            if parent:
                if not hasattr(parent, 'children'):
                    parent.children = []
                parent.children.append(comment)

    root_comments.sort(key=lambda c: -c.score)
    for comment in comments:
        if hasattr(comment, 'children'):
            comment.children.sort(key=lambda c: -c.score)

    return render(
        request,
        "posts/post_detail.html",
        {
            "post": post,
            "community": community,
            "is_owner": is_owner,
            "comments": root_comments,
            "comment_form": CommentCreateForm(),
        },
    )



def delete_post(request, community_name, post_id):
    community = get_object_or_404(Community, name=community_name)
    post = get_object_or_404(Posts, post_id=post_id, community=community)

    if request.user.is_authenticated:
        try:
            app_user = Appuser.objects.get(auth_id=request.user.id)
            if app_user.user_id == post.user_id:
                post.delete()
                messages.success(request, "Post deleted successfully.")
                return redirect('community_home', community_name=community_name)
        except Appuser.DoesNotExist:
            pass

    messages.error(request, "You are not authorized to delete this post.")
    return redirect('post_detail', community_name=community_name, post_id=post_id)


def community_home(request, community_name):
    community = get_object_or_404(Community, name=community_name)
    appuser = Appuser.objects.get(auth_id=request.user.id)

    community_interaction = Usercommunity.objects.filter(
        community_id=community.community_id,
        user_id=appuser.user_id
    )
    joined = True if community_interaction else False
    role = "Visitor" if not community_interaction else community_interaction[0].role
    if request.method == "POST":
        if joined:
            if community_interaction[0].role == "Owner":
                messages.error(
                    request,
                    "Cannot leave a community you own. Designate ownership to another member before leaving."
                )
                return redirect(community_home, community_name=community_name)
            community_interaction[0].delete()
        else:
            Usercommunity.objects.create(
                user_id=appuser.user_id,
                community_id=community.community_id,
                role="Member"
            )
        return redirect('community_home', community_name=community_name)

    posts = Posts.objects.filter(community=community).order_by('-creation_date')

    for post in posts:
        upvotes = PostInteraction.objects.filter(post=post, interaction_type='upvote').count()
        downvotes = PostInteraction.objects.filter(post=post, interaction_type='downvote').count()
        
        post.score = upvotes - downvotes

    return render(request, 'communities/community_home.html', {
        'community': community,
        'joined': joined,
        'posts': posts,
        'role': role
    })

def community_role_edit(request, community_name):
    if not request.user.is_authenticated:
        return redirect("home")
    appuser_id = get_user_id_from_auth_id(request.user.id)
    community_id = Community.objects.get(name=community_name)
    usercommunity = Usercommunity.objects.filter(user_id=appuser_id, community_id=community_id)
    if not usercommunity or usercommunity[0].role != "Owner":
        return redirect(community_home, community_name=community_name)
    # get all members of community
    members = Usercommunity.objects.filter(community_id=community_id).select_related("user").values("role", "user_id", "user__username").order_by("user__username")
    mods = members.filter(role="Moderator")
    owner = members.filter(role="Owner")[0]
    return render(request, 'communities/edit_roles.html', {'members': members, "owner": owner, "mods": mods, "community":community_id, "app_id": appuser_id})

def edit_mods(request, community_name):
    if not request.user.is_authenticated:
        return redirect("home")
    appuser_id = get_user_id_from_auth_id(request.user.id)
    community_id = Community.objects.get(name=community_name)
    usercommunity = Usercommunity.objects.filter(user_id=appuser_id, community_id=community_id)
    if not usercommunity or usercommunity[0].role != "Owner":
        return redirect(community_home, community_name=community_name)
    if request.method == 'POST':
        members = Usercommunity.objects.filter(community_id=community_id).select_related("user")
        for member in members:
            post_name=f"is_{member.user_id}_mod"
            if post_name in request.POST:
                member.role = "Moderator"
            else:
                if member.role != "Owner":
                    member.role = "Member"
            member.save()
        return redirect(community_role_edit, community_name=community_name)
    return redirect(community_home, community_name=community_name)


def profile(request):
    user = request.user
    if user.is_authenticated:
        username = user.username
        appuser = Appuser.objects.get(username=username)
        return render(request, 'profile/profile.html', {'user_profile': appuser})
    else:
        return redirect("home")


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("home")

    username = request.user.username
    appuser = Appuser.objects.get(username=username)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=appuser)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=appuser)

    return render(request, 'profile/edit_profile.html', {'user_profile': appuser, 'form': form})


def get_vote_counts(post_id):
    upvotes = PostInteraction.objects.filter(
        post_id=post_id,
        interaction_type='upvote'
    ).count()

    downvotes = PostInteraction.objects.filter(
        post_id=post_id,
        interaction_type='downvote'
    ).count()

    return {
        'upvotes': upvotes,
        'downvotes': downvotes,
        'score': upvotes - downvotes
    }


def handle_vote(user, post, vote_type):
    try:
        obj, created = PostInteraction.objects.update_or_create(
            user=user,
            post=post,
            defaults={'interaction_type': vote_type}
        )
        return "Vote updated" if not created else "Vote recorded"
    except IntegrityError:
        return "Vote failed"


def vote_post(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        vote_type = request.POST.get("vote_type")
        post = get_object_or_404(Posts, pk=post_id)
        app_user = get_object_or_404(Appuser, auth_id=request.user.id)

        interaction = PostInteraction.objects.filter(user=app_user, post=post).first()
        if interaction:
            if interaction.interaction_type == vote_type:
                interaction.delete()  # remove vote
            else:
                interaction.interaction_type = vote_type
                interaction.save()
        else:
            PostInteraction.objects.create(user=app_user, post=post, interaction_type=vote_type)


        PostInteraction.objects.update_or_create(
            user=Appuser.objects.get(auth_id=request.user.id),
            post=post,
            defaults={'interaction_type': vote_type}
        )

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def add_comment(request, post_id, parent_id=None):
    post = get_object_or_404(Posts, pk=post_id)
    parent = get_object_or_404(Comment, pk=parent_id) if parent_id else None
    appuser_id = get_user_id_from_auth_id(request.user.id)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = appuser_id
            comment.post = post
            comment.reply_to_comment = parent
            comment.creation_date = timezone.now()
            comment.upvotes = 0
            comment.downvotes = 0
            comment.save()
            return redirect("post_detail",
                            community_name=post.community.name,
                            post_id=post.post_id)
    else:
        form = CommentCreateForm()
    return render(request, "comment/comment_form.html",
                  {"form": form, "post": post, "parent": parent,
                   "community": post.community})


@login_required
def edit_comment(request, comment_id):
    appuser_id = get_user_id_from_auth_id(request.user.id)
    comment = get_object_or_404(
        Comment, pk=comment_id, user_id=appuser_id
    )

    community = comment.post.community

    if request.method == "POST":
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post_detail", community_name=community.name, post_id=comment.post_id)
    else:
        form = CommentEditForm(instance=comment)

    return render(
        request,
        "comment/comment_form.html",
        {"form": form, "post": comment.post, "community": community, "editing": True},
    )


@login_required
def delete_comment(request, comment_id):
    appuser_id = get_user_id_from_auth_id(request.user.id)
    comment = get_object_or_404(
        Comment, pk=comment_id, user_id=appuser_id
    )
    post_id = comment.post_id
    community = comment.post.community

    if request.method == "POST":
        comment.delete()
        return redirect("post_detail", community_name=community.name, post_id=post_id)

    return render(
        request,
        "comment/comment_confirm_delete.html",
        {"comment": comment, "community": community},
    )


@login_required
def vote_comment(request, comment_id, direction):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    comment = get_object_or_404(Comment, pk=comment_id)
    voter = get_object_or_404(Appuser, auth_id=request.user.id)

    interaction_type = "upvote" if direction == "up" else "downvote"

    CommentInteraction.objects.update_or_create(
        user=voter,
        comment=comment,
        defaults={"interaction_type": interaction_type},
    )

    up = CommentInteraction.objects.filter(
        comment=comment, interaction_type="upvote"
    ).count()
    dn = CommentInteraction.objects.filter(
        comment=comment, interaction_type="downvote"
    ).count()
    Comment.objects.filter(pk=comment.pk).update(upvotes=up, downvotes=dn)

    html = render_to_string("posts/partials/comment_score.html", {
        "score": up - dn,
        "comment_id": comment.comment_id
    })
    return HttpResponse(html)

@login_required
def edit_post(request, community_name, post_id):
    post = get_object_or_404(Posts, post_id=post_id)
    appuser_id = get_user_id_from_auth_id(request.user.id)

    if post.user_id != appuser_id:
        return HttpResponseForbidden("You do not have permission to edit this post.")

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", community_name=community_name, post_id=post_id)
    else:
        form = PostEditForm(instance=post)

    return render(request, "posts/edit_post.html", {
        "form": form,
        "community_name": community_name,
        "post": post,
    })

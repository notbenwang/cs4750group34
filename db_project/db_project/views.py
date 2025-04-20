from django.shortcuts import render, redirect, get_object_or_404
from db_project.forms import ProfileEditForm, CreateCommunityForm
from db_project.models import Community, Posts, Appuser, Usercommunity
from django.contrib import messages
from django.utils import timezone
from urllib.parse import quote

def get_user_id_from_auth_id(user_id):
    return Appuser.objects.get(auth_id = user_id).user_id

def community_list(request):
    if not request.user.is_authenticated:
        return redirect("home")
    communities = Community.objects.all().order_by('name')
    return render(request, 'communities/communities.html', {'communities' : communities})

def create_community(request):
    if not request.user.is_authenticated:
        return redirect("home")
    new_community = Community()
    
    if request.method == "POST":
        name =  request.POST.get('name')
        about = request.POST.get('about')
        new_community = Community(name=name, about=about, member_count=0)
        form = CreateCommunityForm(request.POST, instance=new_community)
        if form.is_valid():
            form.save()
            creator_role = Usercommunity(user_id = get_user_id_from_auth_id(request.user.id), community_id=new_community.community_id, role="Owner")
            creator_role.save()
            return redirect('community_home', community_name=name)
    else:
        form = CreateCommunityForm(instance=new_community)
    return render(request, 'communities/create_community.html', {'form' : form})

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

def community_home(request, community_name):
    community = get_object_or_404(Community, name=community_name)
    appuser = Appuser.objects.get(auth_id = request.user.id)
    community_interaction = Usercommunity.objects.filter(community_id=community.community_id, user_id = appuser.user_id)
    joined = True if community_interaction else False
    posts = Posts.objects.filter(community=community).order_by('-creation_date')
    
    if request.method == "POST":
        if joined:
            if community_interaction[0].role == "Owner":
                messages.error(request, "Cannot Leave Community you own. Designate ownership to another member before leaving.")
                return render(request, 'communities/community_home.html', {'community' : community, "joined" : joined})
            community_interaction[0].delete()
        if not joined:
            new_status = Usercommunity(user_id=appuser.user_id, community_id=community.community_id, role="Member")
            new_status.save()
        return redirect('community_home', community_name=community_name)
    
    return render(request, 'communities/community_home.html', {'community': community, "joined": joined, 'posts': posts})

def profile(request):
    user = request.user
    if user.is_authenticated:
        username = user.username
        appuser = Appuser.objects.get(username=username)
        return render(request, 'profile/profile.html', {'user_profile' : appuser})
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

    return render(request, 'profile/edit_profile.html', {'user_profile' : appuser, 'form' : form})

from django.shortcuts import render, redirect, get_object_or_404
from db_project.forms import ProfileEditForm, CreateCommunityForm
from db_project.models import Community, Appuser, Usercommunity
from django.contrib import messages

def community_list(request):
    if not request.user.is_authenticated:
        return redirect("home")
    communities = Community.objects.all().order_by('name')
    return render(request, 'communities/communities.html', {'communities' : communities})

def create_community(request):
    if not request.user.is_authenticated:
        return redirect("home")

    return render(request, 'communities/create_community.html')

def update_community_status(request, community_name):
    if not request.user.is_authenticated:
        return redirect("home")
    
    community = get_object_or_404(Community, name=community_name)
    joined = False
    if request.method == "POST":
        appuser = Appuser.objects.get(auth_id = request.user.id)
        community_interaction = Usercommunity.objects.get(community_name=community_name, user_id = appuser.user_id)
        joined = True if community_interaction else False
        print(joined)
        joined = not joined
    return render(request, 'communities/community_home.html', {'community' : community, "joined" : joined})

def community_home(request, community_name):
    community = get_object_or_404(Community, name=community_name)
    appuser = Appuser.objects.get(auth_id = request.user.id)
    community_interaction = Usercommunity.objects.filter(community_id=community.community_id, user_id = appuser.user_id)
    joined = True if community_interaction else False
    
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
    
    return render(request, 'communities/community_home.html', {'community' : community, "joined" : joined})

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

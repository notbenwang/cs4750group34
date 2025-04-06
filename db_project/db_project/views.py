from django.shortcuts import render, redirect, get_object_or_404
from db_project.forms import ProfileEditForm, CreateCommunityForm
from db_project.models import Community, Appuser, Usercommunity

def community_list(request):
    if not request.user.is_authenticated:
        return redirect("home")
    communities = Community.objects.all().order_by('name')
    return render(request, 'communities/communities.html', {'communities' : communities})

def create_community(request):
    if not request.user.is_authenticated:
        return redirect("home")

    return render(request, 'communities/create_community.html')

def join_community(request, community_id):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        appuser = Appuser.objects.get(auth_id = request.user.id)
        community_interaction = Usercommunity.get(community_id=community_id, user_id = appuser.user_id)
        if community_interaction:
            print("delete interaction")
        else:
            print("add interaction")

def view_community_home(request, community_name):
    community = get_object_or_404(Community, name=community_name)
    return render(request, 'communities/community_home.html', {'community' : community})

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

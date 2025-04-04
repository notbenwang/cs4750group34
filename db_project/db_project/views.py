from django.shortcuts import render
from db_project.models import Community

def community_list(request):
    communities = Community.objects.all().order_by('name')
    return render(request, 'communities.html', {'communities' : communities})
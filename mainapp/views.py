from django.shortcuts import render

# Create your views here.
def meber_mgr_view(request):

    return render(request, 'mainapp/member_mgr.html', context={})
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from mainapp.models import GroupType, Member, Staff
from django.contrib.auth import login

@login_required(login_url='mainapp:login')
def member_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    return render(request, 'mainapp/member_mgr.html', context=context)

@csrf_protect
def log_in(request):
    if request.method == "GET":
        return render(request, 'mainapp/member_login.html', context={})
    elif request.method == "POST":
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        staff_user = Staff.objects.get(user__username=uid)
        user = authenticate(username=staff_user.user.username, password=password)
        login(request, user)
        return redirect('mainapp:member')



def ajax_search_member(request):
    if request.method == "GET":
        checkboxs = request.GET.getlist('checkbox[]')
        address = request.GET.get('address')
        mobile = request.GET.get('mobile')
        member_name = request.GET.get('member_name')
        dic = {}
        dic['name'] = member_name
        dic['mobile'] = mobile
        dic['address'] = address
        #dic['group_type__name__in'] = checkboxs
        # 변수를 넘길때 * 1개 or * 2개 형식이 있음. *args or **kwargs 참조
        member = Member.objects.filter(
            (Q(name__contains=member_name) | Q(mobile__contains=mobile) | Q(address__contains=address)) & Q(group_type__name__in=checkboxs))

        data = serialize("json", member)
        return JsonResponse({'status': 'success', 'data': data})
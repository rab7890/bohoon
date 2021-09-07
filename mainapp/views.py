from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, logout

from mainapp.forms import MemberForm
from mainapp.models import GroupType, Member, Staff
from django.contrib.auth import login

@login_required(login_url='mainapp:login')
def member_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    return render(request, 'mainapp/member_mgr.html', context=context)

@login_required(login_url='mainapp:login')
def event_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    context['participate'] = ['위문품(설)', '위문품(보훈)', '위문품(추석)', '위문품(기타1)', '위문품(기타2)', '위문품(기타2)',
                              '전적지순례', '체련대회']

    return render(request, 'mainapp/event_mgr.html', context=context)

@login_required(login_url='mainapp:login')
def member_detail_view(request, pk):
    context = {}
    obj = Member.objects.get(id=pk)
    context['member'] = obj
    return render(request, 'mainapp/member_detail.html', context=context)

@csrf_protect
@login_required(login_url='mainapp:login')
def member_register_view(request):
    if request.method == "GET":
        context = {}
        context['form'] = MemberForm()
        return render(request, 'mainapp/member_detail.html', context=context)
    else:
        form = MemberForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponse('<script type="text/javascript">window.close();</script>')


@csrf_protect
def log_in(request):
    if request.method == "GET":
        return render(request, 'mainapp/member_login.html', context={})
    elif request.method == "POST":

        uid = request.POST.get('uid')
        password = request.POST.get('password')

        staff_user = Staff.objects.get(user__username=uid)
        if staff_user.user.check_password(password):
            user = authenticate(request=request, username=staff_user.user.username, password=password)
            login(request, user)
            return redirect('mainapp:member')
        else:
            return render(request, 'mainapp/member_login.html', context={})


def log_out(request):
    if request.method == "GET":
        logout(request)
        return render(request, 'mainapp/member_login.html', context={})




def ajax_search_member(request):
    if request.method == "GET":
        checkboxs = request.GET.getlist('checkbox[]')
        address = request.GET.get('address')
        mobile = request.GET.get('mobile')
        member_name = request.GET.get('member_name')
        dic = {}
        dic['name__contains'] = member_name
        dic['mobile__contains'] = mobile
        dic['address__contains'] = address
        delete = [key for key in dic if not dic[key]]
        for key in delete:
            del dic[key]
        """
        queries = Q(cnp=cnp)
        if phone:
            queries |= Q(phones__contains=[phone])
        if email:
            queries |= Q(emails__contains=[email])
        """
        #dic['group_type__name__in'] = checkboxs
        # 변수를 넘길때 * 1개 or * 2개 형식이 있음. *args or **kwargs 참조
        member = Member.objects.filter(**dic).filter(group_type__name__in=checkboxs)

        data = serialize("json", member)
        return JsonResponse({'status': 'success', 'data': data})
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, logout
from rest_framework import serializers

from mainapp.forms import MemberForm
from mainapp.models import GroupType, Member, Staff, GroupEvent
from django.contrib.auth import login
from django.db.models import CharField, Value


@login_required(login_url='mainapp:login')
def member_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    return render(request, 'mainapp/member_mgr.html', context=context)



@login_required(login_url='mainapp:login')
def member_detail_view(request, pk):
    context = {}
    if request.method == "GET":
        obj = Member.objects.get(id=pk)
        context['form'] = MemberForm(instance=obj)
        context['member'] = obj
        return render(request, 'mainapp/member_detail.html', context=context)
    else:
        form = MemberForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponse('<script type="text/javascript">window.close(); location.reload();</script>')

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

class GroupEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupEvent
        fields = '__all__'
        depth = 2


@login_required(login_url='mainapp:login')
def event_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    context['participate'] = ['위문품(설)', '위문품(보훈)', '위문품(추석)', '위문품(기타1)', '위문품(기타2)', '위문품(기타3)',
                              '전적지순례', '체련대회']

    return render(request, 'mainapp/event_mgr.html', context=context)

@login_required(login_url='mainapp:login')
def event_register_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s

    return render(request, 'mainapp/event_register.html', context=context)


def ajax_search_member_by_event(request):
    if request.method == "GET":
        ck_group = request.GET.getlist('ck_group[]')
        ck_participant = request.GET.getlist('ck_participant[]')
        event_date = request.GET.get('event_date')
        member_name = request.GET.get('member_name')
        fileds = {'위문품(설)': 'sul', '위문품(보훈)': 'bohoon', '위문품(추석)': 'choosuk', '위문품(기타1)': 'etc1',
                  '위문품(기타2)': 'etc2', '위문품(기타3)':'etc3', '전적지순례': 'junjukji', '체련대회': 'charun'}
        d = {}

        for k in fileds:
            if k in ck_participant:
                d[fileds[k]] = True
            else:
                d[fileds[k]] = False

        ge = GroupEvent.objects.filter(member__group_type__name__in=ck_group, member__name=member_name,
                                       event_created_date=event_date, **d)

        data = GroupEventSerializer(ge, many=True)

        return JsonResponse({'status': 'success', 'data': data.data})

@csrf_protect
def ajax_modify_group_event(request):
    if request.method == "POST":

        gid = request.POST.get('gid')
        sul = request.POST.get('ck_sul')
        bohoon = request.POST.get('ck_bohoon')
        choosuk = request.POST.get('ck_choosuk')
        etc1 = request.POST.get('ck_etc1')
        etc2 = request.POST.get('ck_etc2')
        etc3 = request.POST.get('ck_etc3')
        junjukji = request.POST.get('ck_junjukji')
        charun = request.POST.get('ck_charun')
        ge = GroupEvent.objects.get(id=gid)
        ge.sul = sul
        ge.bohoon = bohoon
        ge.choosuk = choosuk
        ge.etc1 = etc1
        ge.etc2 = etc2
        ge.etc3 = etc3
        ge.junjukji = junjukji
        ge.charun = charun
        ge.save()

        return JsonResponse({'status': 'success', 'error': ""})

@csrf_protect
def ajax_add_group_event(request):
    if request.method == "POST":

        id_list = request.POST.getlist('id_list[]')
        event_date = request.POST.get('event_date')
        for pk in id_list:
            ge = GroupEvent()
            ge.member_id = pk
            ge.event_created_date = event_date
            ge.sul = False
            ge.bohoon = False
            ge.choosuk = False
            ge.etc1 = False
            ge.etc2 = False
            ge.etc3 = False
            ge.junjukji = False
            ge.charun = False
            ge.save()

        return JsonResponse({'status': 'success', 'error': ""})
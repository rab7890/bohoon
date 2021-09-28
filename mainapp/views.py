import tempfile

import xlrd
import xlwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, logout
from rest_framework import serializers

from mainapp.serializers import GroupEventSerializer, MemberSerializer
from mainapp.forms import MemberForm
from mainapp.models import GroupType, Member, Staff, GroupEvent
from django.contrib.auth import login
from django.db.models import CharField, Value




@login_required(login_url='login')
def member_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    return render(request, 'mainapp/member_mgr.html', context=context)



@login_required(login_url='login')
def member_detail_view(request, pk):
    context = {}
    if request.method == "GET":
        obj = Member.objects.get(id=pk)
        context['form'] = MemberForm(instance=obj)
        context['member'] = obj
        return render(request, 'mainapp/member_detail.html', context=context)
    else:
        pk = request.POST.get('pk')
        obj = Member.objects.get(id=pk)
        form = MemberForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('mainapp:member')


@csrf_protect
@login_required(login_url='login')
def member_register_view(request):
    if request.method == "GET":
        context = {}
        u = request.user
        s = Staff.objects.get(user=u)
        context['staff'] = s
        context['form'] = MemberForm()

        return render(request, 'mainapp/member_register.html', context=context)
    else:
        form = MemberForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponse('<script type="text/javascript">window.close();</script>')

"""
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
"""

def event_sel_mem(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    return render(request, 'mainapp/event_sel_mem.html', context=context)


def ajax_search_member(request):
    if request.method == "GET":
        checkboxs = request.GET.getlist('checkbox[]')
        address = request.GET.get('address')
        mobile = request.GET.get('mobile')
        member_name = request.GET.get('member_name')
        memo = request.GET.get('memo')
        
        dic = {}
        dic['name__contains'] = member_name
        dic['mobile__contains'] = mobile
        dic['address__contains'] = address
        dic['memo__contains'] = memo
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
        member = Member.objects.filter(**dic).filter(group_type__name__in=checkboxs)[:200]

         
    
        data = MemberSerializer(member, many=True)
    return JsonResponse({'status': 'success', 'data': data.data})

def ajax_search_member_sel(request):
    if request.method == "GET":
        checkboxs = request.GET.getlist('checkbox[]')
        address = request.GET.get('address')
        mobile = request.GET.get('mobile')
        member_name = request.GET.get('member_name')
        memo = request.GET.get('memo')
        
        dic = {}
        dic['name__contains'] = member_name
        dic['mobile__contains'] = mobile
        dic['address__contains'] = address
        dic['memo__contains'] = memo
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
        member = Member.objects.filter(**dic).filter(group_type__name__in=checkboxs)[:200]

        data = MemberSerializer(member, many=True)
    return JsonResponse({'status': 'success', 'data': data.data})


@login_required(login_url='mainapp:login')
def event_mgr_view(request):
    context = {}
    u = request.user
    s = Staff.objects.get(user=u)
    context['staff'] = s
    context['participate'] = ['설', '보훈', '추석','전적지순례', '체련대회', '기타1', '기타2', '기타3']

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
        fileds = {'설': 'sul', '보훈': 'bohoon', '위문품(추석)': 'choosuk', '위문품(기타1)': 'etc1',
                  '위문품(기타2)': 'etc2', '위문품(기타3)':'etc3', '전적지순례': 'junjukji', '체련대회': 'charun'}
        d = {}

        for k in fileds:
            if k in ck_participant:
                d[fileds[k]] = True
            else:
                d[fileds[k]] = False
        dic = {}
        #or_queries = [Q(**{lookup: value}) for lookup in lookups]
        dic['member__name__contains'] = member_name
        dic['event_created_date'] = event_date
        delete = [key for key in dic if not dic[key]]
        for key in delete:
            del dic[key]
        ge = GroupEvent.objects.filter(member__group_type__name__in=ck_group, **dic)[:200]
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
        explain = request.POST.get('ck_explain') 
        ge = GroupEvent.objects.get(id=gid)
        ge.sul = sul
        ge.bohoon = bohoon
        ge.choosuk = choosuk
        ge.etc1 = etc1
        ge.etc2 = etc2
        ge.etc3 = etc3
        ge.junjukji = junjukji
        ge.charun = charun
        ge.explain = explain
        ge.save()

        return JsonResponse({'status': 'success', 'error': ""})

@csrf_protect
def ajax_del_group_event(request):
    if request.method == "POST":

        gid = request.POST.get('gid')
        
        ge = GroupEvent.objects.get(id=gid)
        ge.delete()

        return JsonResponse({'status': 'success', 'error': ""})

@csrf_protect
def ajax_add_group_event(request):
    if request.method == "POST":

        id_list = request.POST.getlist('id_list[]')
        event_date = request.POST.get('event_date')

        for pk in id_list:
            if GroupEvent.objects.filter(member_id=pk, event_created_date=event_date).exists():
                continue
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

def save_excel(request):
    if request.method == "GET":

        response = HttpResponse(content_type='application/ms-excel')

        # decide file name
        response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xls"'

        # creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        # adding sheet
        ws = wb.add_sheet("sheet1")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        # column header names, you can use your own headers here
        #columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4', ]
        columns = []
        for field in Member._meta.fields:
            columns.append(field.name)
        # write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        # get your data, from database or from a text file...
        members = Member.objects.all()[:10]
        for member_obj in members:
            row_num = row_num + 1
            ws.write(row_num, 0, member_obj.id, font_style)
            ws.write(row_num, 1, member_obj.name, font_style)
            ws.write(row_num, 2, member_obj.birth_date, font_style)
            #ws.write(row_num, 2, my_row.end_date_time, font_style)
            #ws.write(row_num, 3, my_row.notes, font_style)
            ws.write(row_num, 18, member_obj.group_type.name, font_style)

        wb.save(response)
        return response

@csrf_protect
def upload_excel(request):
    if request.method == "POST":
        xlsfile = request.FILES.get('file', None)
        """
        tempfn = tempfile.TemporaryFile(prefix='contact-import')
        with open(tempfn, 'wb+') as destination:
            for chunk in xlsfile.chunks():
                destination.write(chunk)
        """
        with tempfile.TemporaryFile() as f:
            with open(f, 'wb+') as destination:
                for chunk in xlsfile.chunks():
                    destination.write(chunk)
            wb = xlrd.open_workbook(f)
        # now open the file by reading from the temp file


        return JsonResponse({'status': 'success', 'error': ""})
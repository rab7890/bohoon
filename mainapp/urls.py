from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('member', views.member_mgr_view, name='member'),
    path('member/<int:pk>', views.member_detail_view, name='member_detail'),
    path('member/register', views.member_register_view, name='member_register'),
    path('member/excel/save', views.save_excel, name='member_save_excel'),

    path('member/excel/upload', views.upload_excel, name='member_upload_excel'),

    path('ajax/member/search', views.ajax_search_member, name='ajax_search_member'),
    path('ajax/member/search2', views.ajax_search_member, name='ajax_search_member2'),

    path('event', views.event_mgr_view, name='event'),
    path('event/select', views.event_sel_mem, name='event_sel_mem'),
    path('event/register', views.event_register_view, name='register_event'),
    path('ajax/event/member/search', views.ajax_search_member_by_event, name='ajax_search_group_event'),
    path('ajax/event/modify', views.ajax_modify_group_event, name='ajax_modify_event'),
    path('ajax/event/delete', views.ajax_del_group_event, name='ajax_del_event'),
    path('ajax/event/add', views.ajax_add_group_event, name='ajax_add_event'),
    
    path('ajax/event/member2/search', views.ajax_search_member_sel, name='ajax_search_member_sel'),

]

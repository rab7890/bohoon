from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('member', views.member_mgr_view, name='member'),
    path('ajax/member/search', views.ajax_search_member, name='ajax_search_member'),

    path('login', views.log_in, name='login'),
]
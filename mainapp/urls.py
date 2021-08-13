from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('member', views.meber_mgr_view, name='member')
]
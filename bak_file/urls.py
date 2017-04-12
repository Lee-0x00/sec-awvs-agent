#-*- coding: UTF-8 -*- 
#__author__:Bing
#email:amazing_bing@outlook.com


from django.conf.urls import include, url
from aws_scan import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^wvs_scan_list/', views.wvs_scan_list,name='wvs_scan_list'),
    url(r'^wvs_scan_add/', views.wvs_scan_add,name='wvs_scan_add'),
    url(r'^wvs_scan_getresult/', views.wvs_scan_getresult,name='wvs_scan_getresult'),
    url(r'^wvs_scan_pause/', views.wvs_scan_pause,name='wvs_scan_pause'),
    url(r'^wvs_scan_resume/', views.wvs_scan_resume,name='wvs_scan_resume'),
    url(r'^wvs_scan_del/', views.wvs_scan_del,name='wvs_scan_del'),
    url(r'^big_file_download/', views.big_file_download,name='big_file_download'),
#     url(r'^add_task/', views.index,name='add'),
#     url(r'^add_task/', views.index,name='add'),
]

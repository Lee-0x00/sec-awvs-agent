#-*- coding: UTF-8 -*- 
#__author__:Bing
#email:amazing_bing@outlook.com

from django.shortcuts import render_to_response,HttpResponse,HttpResponseRedirect,Http404
from django.http import JsonResponse
from aws_scan.models import AWVSTask

def index(request):
    return HttpResponse("Welcome,This is awvs_scan api .")


#===============================================================================
# wvs task excute views 
#===============================================================================
def wvs_scan_list(request):
    task = AWVSTask()
    result = task.awvs_list_mod()
    
    status = result["status"]
    #print result
    if status == 1 :
        return JsonResponse(result)
    else:
        return JsonResponse({"status": 0})


def wvs_scan_add(request):
    #taskid = str(request.GET.get('taskid',""))
    domain = request.GET.get('domain',"")
    
    if domain != "" and domain.startswith("http://",0,8) or domain.startswith("https://",0,8):
        task = AWVSTask()
        #result = task.awvs_add_mod(domain,scantype=0,cookies="<none>")
        result = task.awvs_add_mod(domain)
        
        status = result["status"]
        #print result
        if status == 1 :
            return JsonResponse(result)
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 2,"data":[{"msg":"please,no parameter or  format is error!"}]})


def wvs_scan_pause(request):
    id = request.GET.get('id',"")
    if id != "":
        task = AWVSTask()
        result = task.awvs_pause_mod(id)
        
        status = result["status"]
        #print result
        if status == 1 :
            return JsonResponse(result)
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 2,"data":[{"msg":"please,no parameter or  format is error!"}]})


def wvs_scan_resume(request):
    id = request.GET.get('id',"")
    if id != "":
        task = AWVSTask()
        result = task.awvs_resume_mod(id)
        
        status = result["status"]
        #print result
        if status == 1 :
            return JsonResponse(result)
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 2,"data":[{"msg":"please,no parameter or  format is error!"}]})




def wvs_scan_getresult(request):
    id = request.GET.get('id',"")
    path_file = request.GET.get('path_file',"")
    if path_file != "" and id != "":
        task = AWVSTask()
        result = task.awvs_getresult_mod(id, path_file)
        
        status = result["status"]
        #print result
        if status == 1 :
            return JsonResponse(result)
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 2,"data":[{"msg":"please,no parameter or  format is error!"}]})


def wvs_scan_del(request):
    id = request.GET.get('id',"")
    if id != "":
        task = AWVSTask()
        result = task.awvs_del_mod(id)
        
        status = result["status"]
        #print result
        if status == 1 :
            return JsonResponse(result)
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 2,"data":[{"msg":"please,no parameter or  format is error!"}]})
    




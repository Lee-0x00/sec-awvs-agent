#-*- coding: UTF-8 -*- 
#__author__:Bing
#email:amazing_bing@outlook.com

from django.shortcuts import render_to_response,HttpResponse,HttpResponseRedirect,Http404
from django.http import StreamingHttpResponse
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
    scantype = request.GET.get('scantype',0)
    cookies =  request.GET.get('cookie',"<none>")

    if domain != "" and domain.startswith("http://",0,8) or domain.startswith("https://",0,8):
        task = AWVSTask()
        #result = task.awvs_add_mod(domain,scantype=0,cookies="<none>")
        result = task.awvs_add_mod(domain,scantype,cookies)
        
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
    id = request.GET.get('id', "")
    file_name = request.GET.get('file_name', "")
    if file_name != "" and id != "":
        task = AWVSTask()
        result = task.awvs_getresult_mod(id, file_name)

        status = result["status"]
        # print result
        if status == 1:
            result_file_path = result["data"]
            code = ""
            with open("{0}".format(result_file_path), "rb") as f:
                code = f.read()

            the_file_name = "{0}".format(str(result_file_path.split("\\")[-1]))
            # print "D:\\awvs\\{0}".format(str(path_file))
            response = StreamingHttpResponse(code)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
            return response
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 2, "data": [{"msg": "please,no parameter or  format is error!"}]})


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
    


def big_file_download(request):
    path_file = request.GET.get('path_file',"")
    if id != "":
        code = ""
        with open("D:\\awvs\\{0}".format(str(path_file)),"rb") as f:
            code = f.read()

        the_file_name = "{0}".format(str(path_file))
        #print "D:\\awvs\\{0}".format(str(path_file))
        response = StreamingHttpResponse(code)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

        return response
    else:
        return JsonResponse({"status": 2, "data": [{"msg": "please,no parameter or  format is error!"}]})



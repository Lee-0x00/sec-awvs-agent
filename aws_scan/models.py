#-*- coding: UTF-8 -*- 
#__author__:Bing
#email:amazing_bing@outlook.com

import httplib,json,urllib2
from datetime import datetime
from time import gmtime, strftime

class AWVSTask:
    def __init__(self):
        self.api_url = "127.0.0.1"
        self.api_port = 8183
        self.api_header = {
                            "Content-Type": "application/json; charset=UTF-8",
                            "X-Requested-With": "XMLHttpRequest",
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "RequestValidated": "true"
                        }

    #this is  ok 
    def awvs_list_mod(self):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        conn.request("GET", "/api/listScans", headers=self.api_header)
        resp = conn.getresponse()
        content = resp.read()
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            content = []
            
            task_count = result["data"]["count"].encode("gbk")
            for i in result["data"]["scans"] :
                task_id = i["id"].encode("gbk")
                task_target =  i["target"].encode("gbk")
                task_module =  i["profile"].encode("gbk")
                task_process =  i["progress"]
                task_risk =  self.awvs_getrisk_mod(task_id,task_target)["data"]
                task_status =  i["status"].encode("gbk")
                #print task_count,task_id,task_target,task_module,task_process,task_node,task_risk,task_status,ids
                content.append({"task_count":task_count,"task_id":task_id,"task_target":task_target,"task_module":task_module,"task_risk":task_risk,"task_process":task_process,"task_status":task_status})
            return {"status":1,"data":content}
        else:
            return {"status":0}

    #this is  ok 
    def awvs_add_mod(self,domain,scantype=0,cookies="<none>"):
        scan_type = ["Default","Sql_Injection","XSS"]
        ACUDATA = {"scanType":"scan",
                   "targetList":"",
                   "target":["%s" % domain],
                   "recurse":"-1",
                   "date":strftime("%m/%d/%Y", gmtime()),
                   "dayOfWeek":"1",
                   "dayOfMonth":"1",
                   "time": "%s:%s" % (datetime.now().hour, datetime.now().minute+2),
                   "deleteAfterCompletion":"False",
                   "params":{"profile":str(scan_type[scantype]),
                             "loginSeq":str(cookies),
                             "settings":"Default",
                             "scanningmode":"heuristic",
                             "excludedhours":"<none>",
                             "savetodatabase":"True",
                             "savelogs":"False",
                             "generatereport":"True",
                             "reportformat":"PDF",
                             "reporttemplate":"WVSDeveloperReport.rep",
                             "emailaddress":""}
                   }

        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        conn.request("POST", "/api/addScan", json.dumps(ACUDATA) , self.api_header)
        resp = conn.getresponse()
        content = resp.read()
        #{"result":"FAIL","errorMessage":"invalid website URL!"}
        #{"result":"OK","data":["6"]}
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            content = result["data"][0].encode("gbk")
            return {"status":1,"data":content}
        else:
            return {"status":0}



    def awvs_resume_mod(self,id):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({"id":str(id)})
        conn.request("POST", "/api/resumeScan", data, self.api_header)
        # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
        resp = conn.getresponse()
        content = resp.read()
        
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            return {"status":1}
        else:
            return {"status":0}


    def awvs_pause_mod(self,id):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({"id":str(id)})
        conn.request("POST", "/api/pauseScan", data, self.api_header)
        resp = conn.getresponse()
        content = resp.read()
        
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            return {"status":1}
        else:
            return {"status":0}

    def awvs_stop_mod(self,id):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({"id":str(id)})
        conn.request("POST", "/api/stopScan", data, self.api_header)
        # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
        resp = conn.getresponse()
        content = resp.read()
        
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            return {"status":1}
        else:
            return {"status":0}


    def awvs_del_mod(self,id):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({'id': str(id), 'deleteScanResults': 1})
        conn.request("POST", "/api/deleteScan", data, self.api_header)
        resp = conn.getresponse()
        content = resp.read()
        #{"result":"OK"}
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            return {"status":1}
        else:
            return {"status":0}


    def awvs_getresult_mod(self,id,path_file):
        # conn = httplib.HTTPConnection(self.api_url, self.api_port)
        # data = json.dumps({"id":str(id)})
        # conn.request("POST", "/api/getScanResults", data , self.api_header)
        # # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
        # resp = conn.getresponse()
        # content = resp.read()
        
        # status = resp.status
        # if status == 200 and "OK" in content :
        #     #{"result":"OK","data":[{"id":"2d1484299b7fc582b54ff75c3b0b33dd","date":"周三 29 三月 2017, 13:39:36","size":"195.75 KB"}]}
        #     reportid = eval(content)["data"][0]["id"]
        #     conn.request("GET", "/api/download/{0}:{1}".format(id, reportid), headers=self.api_header)
        #     resp = conn.getresponse()
        #     report_contents = resp.read()
        #     print report_contents
        #     return 1
        # else:
        #     return 0
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({"id":str(id)})
        conn.request("POST", "/api/getScanResults", data , self.api_header)
        # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
        resp = conn.getresponse()
        content = resp.read()

        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            try:
                reportid = result["data"][0]["id"].encode("gbk")
                conn.request("GET", "/api/download/{0}:{1}".format(id, reportid), headers=self.api_header)
                resp = conn.getresponse()
                download_contents = resp.read()
                #print download_contents
                #return {"status":1,"data":download_contents}
                save_file = self.download(path_file="D:\\awvs\\{0}.zip".format(str(path_file)),data=download_contents)
                if save_file['status'] == 1:
                    return {"status":1,"data":"{0}.zip".format(str(path_file))}
                else:
                    return {"status":2}
            except:
                return {"status":0}
        else:
            return {"status":0}


    #this is  ok 
    def awvs_getrisk_mod(self,id,domain):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        conn.request("POST", "/api/getScanHistory", json.dumps({'id': str(id)}), headers=self.api_header)
        # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
        resp = conn.getresponse()
        content = resp.read()
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            content = ""
            for line in result["data"]:
                msg = line["msg"].encode("gbk")
                if str(domain) in msg :
                    arr = msg.split(",")
                    content = '{0}{1}{2}'.format(arr[0][-6:],arr[1],arr[2])
            return {"status":1,'data':content}
        else:
            return {"status":0}

    def download(self,path_file,data):
        try:
            with open("{0}".format(path_file), "wb") as code:     
                code.write(data)
                code.close()
            return {"status":1,"data":path_file}
        except:
            return {"status":0}

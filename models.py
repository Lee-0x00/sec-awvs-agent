#-*- coding: UTF-8 -*- 
#__author__:Bing
#email:amazing_bing@outlook.com

import httplib,json,urllib2
from datetime import datetime
from time import gmtime, strftime
from xml.dom import minidom
import random,time
import os,sys
import zipfile

#判断是否为域名
def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', re.IGNORECASE)
    return True if domain_regex.match(domain) else False

#判断是否为ip
def is_host(host):
    ip_regex = re.compile(r'(^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$)', re.IGNORECASE)
    return True if ip_regex.match(host) else False

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
        self.filter = {
                            "color_white_list": ["orange", "red"],  # green,blue,orange,red四种级别
                            "bug_black_list": [                     # 漏洞黑名单，过滤掉一些危害等级高，但没什么卵用的洞
                                "User credentials are sent in clear text"
                            ]
                        }

    def parse_xml(self,file_name):
        bug_list = []

        try:
            root = minidom.parse(file_name).documentElement
            #print dir(root),"**********"
            #print root.nodeName,root.nodeValue,root.nodeType
            ReportItem_list =  root.getElementsByTagName('ReportItem')
            #print root.getElementsByTagName('ScanTime')[0].firstChild.data.encode('utf-8')
            if ReportItem_list:
                for node in ReportItem_list:
                    color = node.getAttribute("color")
                    name = node.getElementsByTagName("Name")[0].firstChild.data.encode('utf-8')
                    #print color,name
                    if color in self.filter['color_white_list'] and name not in self.filter['bug_black_list']:
                        temp = {}
                        temp['name'] = name
                        temp['color'] = color.encode('utf-8')
                        temp['details'] = node.getElementsByTagName("Details")[0].firstChild.data.encode('utf-8')
                        temp['affect'] = node.getElementsByTagName("Affects")[0].firstChild.data.encode('utf-8')
                        temp['severity'] = node.getElementsByTagName("Severity")[0].firstChild.data.encode('utf-8')
                        temp['request'] = node.getElementsByTagName("Request")[0].firstChild.data.encode('utf-8')
                        temp['response'] = node.getElementsByTagName("Response")[0].firstChild.data.encode('utf-8')
                        temp['repair'] = ""
                        #print bug_list,temp
                        bug_list.append(temp)
        except Exception, e:
            return {"status":0}

        result = {"status":1,"data":bug_list}
        return result


    def download(self,path_file,data):
        try:
            with open("{0}".format(path_file), "wb") as code:     
                code.write(data)
                code.close()
            return {"status":1,"data":path_file}
        except:
            return {"status":0}

    def awvs_count(self):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        conn.request("GET", "/api/listScans", headers=self.api_header)
        resp = conn.getresponse()
        content = resp.read()
        result = json.loads(content)

        status = result["result"].encode("gbk")
        if status == "OK":          
            task_count = result["data"]["count"].encode("gbk")
            return {"status":1,"data":task_count}
        else:
            return {"status":1}



    def awvs_add(self,profile,loginSeq,target):
        scan_type = ["Default","Sql_Injection","XSS"]
        try:
            ACUDATA = {"scanType":"scan",
                       "targetList":"",
                       "target":["%s" % target],
                       "recurse":"-1",
                       "date":strftime("%m/%d/%Y", gmtime()),
                       "dayOfWeek":"1",
                       "dayOfMonth":"1",
                       "time": "%s:%s" % (datetime.now().hour, datetime.now().minute+2),
                       "deleteAfterCompletion":"False",
                       "params":{"profile":str(scan_type[int(profile)]),
                                 "loginSeq":str(loginSeq),
                                 "settings":"Default",
                                 "scanningmode":"heuristic",
                                 "excludedhours":"<none>",
                                 "savetodatabase":"False",
                                 "savelogs":"False",
                                 "ExportXML":"tt.xml",
                                 # "generatereport":"True",
                                 # "reportformat":"RTF",
                                 # "reporttemplate":"WVSDeveloperReport.rep",
                                 "emailaddress":""}
                       }
        except:
            return {"status":0}

        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        conn.request("POST", "/api/addScan", json.dumps(ACUDATA) , self.api_header)
        resp = conn.getresponse()
        content = resp.read()

        #请求增加任务
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            taskid = result["data"][0].encode("gbk")
            return {"status":1,"data":taskid}
        else:
            return {"status":0}


    def awvs_report(self,taskid,save_dir="m:\\"):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({"id":str(taskid)})
        conn.request("POST", "/api/getScanResults", data , self.api_header)
        resp = conn.getresponse()
        content = resp.read()

        #请求下载报告
        result = json.loads(content)
        status = result["result"].encode("gbk")
        result_len = len(result["data"][0])

        print result_len,result["data"]
        if status == "OK" and result_len == 3:
            #print "te"
            try:
                report_id = result["data"][0]["id"].encode("gbk")
                #http://localhost:8183/api/download/5:ac1e564ca8da24f1c94432cac9ee6553
                conn.request("GET", "/api/download/{0}:{1}".format(taskid, report_id), headers=self.api_header)
                resp = conn.getresponse()
                download_contents = resp.read()

                #保持报告文件
                random_file_name = strftime("%Y%m%d-%H%M%S", time.localtime())  #待修改为日期文件
                #print strftime("%Y%m%d-%H%M%S", time.localtime())
                zipfilename = "{0}{1}.zip".format(str(save_dir),str(random_file_name))
                xmlfilename = "{0}{1}.xml".format(str(save_dir),str(random_file_name))

                download_file = self.download(path_file=zipfilename,data=download_contents)
                if download_file['status'] == 1:
                    xml_filename = self.unzip_dir(unzipfilename=zipfilename,savexmlfile=xmlfilename)
                    if xml_filename["status"] == 1:
                        os.remove(zipfilename)
                        xml_data = self.parse_xml(xml_filename["data"])
                        if xml_data['status'] == 1:
                            os.remove(xmlfilename)
                            print xml_data
                            return {"status":1,"data":xml_data["data"]}
                else:
                    return {"status":2}
            except:
                return {"status":0}
        else:
            return {"status":0}


    def awvs_delete(self,taskid):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({'id': str(taskid), 'deleteScanResults': 1})
        conn.request("POST", "/api/deleteScan", data, self.api_header)
        resp = conn.getresponse()
        content = resp.read()

        #删除任务
        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            return {"status":1}
        else:
            return {"status":0}


    def awvs_process(self,taskid):
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        conn.request("GET", "/api/listScans", headers=self.api_header)
        resp = conn.getresponse()
        content = resp.read()

        result = json.loads(content)
        status = result["result"].encode("gbk")
        if status == "OK":
            task_process = ""
            for i in result["data"]["scans"] :
                task_id = i["id"].encode("gbk")
                if str(task_id) == str(taskid):
                    task_process =  i["progress"]
            return {"status":1,"data":task_process}
        else:
            return {"status":0}


    def awvs_list_loginseq(self):
        cookie_dir = "C:\Users\Public\Documents\Acunetix WVS 10\LoginSequences"
        content = []
        for parent,dirnames,filenames in os.walk(cookie_dir):
            for filename in filenames:
                content.append(filename)
        result = {"status":1,"data":content}
        return result



    def unzip_dir(self,unzipfilename, savexmlfile):
        #fullzipfilename = os.path.abspath(unzipfilename) 
        #fullunzipdirname = os.path.abspath(savexmlfile)  
        #print fullzipfilename
        result = ""
        try:
            srcZip = zipfile.ZipFile(unzipfilename, "r")
            for eachfile in srcZip.namelist():
                if eachfile.endswith(".xml",3):
                    fd=open(savexmlfile, "wb")
                    result = savexmlfile
                    print result
                    fd.write(srcZip.read(eachfile))
                    fd.close()
                else:
                    pass

            srcZip.close()
            return {"status":1,"data":result}
        except:
          return {"status":0}



# AWVSTask().awvs_add(1,"test.lsr","http://www.wakeuppeople.top")
#AWVSTask().awvs_report(5)
#AWVSTask().unzip_dir(unzipfilename="M:\\0.zip")
#AWVSTask().parse_xml("M:\\5.xml")
#print AWVSTask().awvs_list_loginseq()












    # #this is  ok 
    # def awvs_list_mod(self):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     conn.request("GET", "/api/listScans", headers=self.api_header)
    #     resp = conn.getresponse()
    #     content = resp.read()
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         content = []
            
    #         task_count = result["data"]["count"].encode("gbk")
    #         for i in result["data"]["scans"] :
    #             task_id = i["id"].encode("gbk")
    #             task_target =  i["target"].encode("gbk")
    #             task_module =  i["profile"].encode("gbk")
    #             task_process =  i["progress"]
    #             task_risk =  self.awvs_getrisk_mod(task_id,task_target)["data"]
    #             task_status =  i["status"].encode("gbk")
    #             #print task_count,task_id,task_target,task_module,task_process,task_node,task_risk,task_status,ids
    #             content.append({"task_count":task_count,"task_id":task_id,"task_target":task_target,"task_module":task_module,"task_risk":task_risk,"task_process":task_process,"task_status":task_status})
    #         return {"status":1,"data":content}
    #     else:
    #         return {"status":0}

    # #this is  ok 
    # def awvs_add_mod(self,domain,scantype=0,cookies="<none>"):
    #     scan_type = ["Default","Sql_Injection","XSS"]
    #     ACUDATA = {"scanType":"scan",
    #                "targetList":"",
    #                "target":["%s" % domain],
    #                "recurse":"-1",
    #                "date":strftime("%m/%d/%Y", gmtime()),
    #                "dayOfWeek":"1",
    #                "dayOfMonth":"1",
    #                "time": "%s:%s" % (datetime.now().hour, datetime.now().minute+2),
    #                "deleteAfterCompletion":"False",
    #                "params":{"profile":str(scan_type[int(scantype)]),
    #                          "loginSeq":str(cookies),
    #                          "settings":"Default",
    #                          "scanningmode":"heuristic",
    #                          "excludedhours":"<none>",
    #                          "savetodatabase":"True",
    #                          "savelogs":"False",
    #                          "generatereport":"True",
    #                          "reportformat":"PDF",
    #                          "reporttemplate":"WVSDeveloperReport.rep",
    #                          "emailaddress":""}
    #                }

    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     conn.request("POST", "/api/addScan", json.dumps(ACUDATA) , self.api_header)
    #     resp = conn.getresponse()
    #     content = resp.read()
    #     #{"result":"FAIL","errorMessage":"invalid website URL!"}
    #     #{"result":"OK","data":["6"]}
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         content = result["data"][0].encode("gbk")
    #         return {"status":1,"data":content}
    #     else:
    #         return {"status":0}



    # def awvs_resume_mod(self,id):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     data = json.dumps({"id":str(id)})
    #     conn.request("POST", "/api/resumeScan", data, self.api_header)
    #     # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
    #     resp = conn.getresponse()
    #     content = resp.read()
        
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         return {"status":1}
    #     else:
    #         return {"status":0}


    # def awvs_pause_mod(self,id):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     data = json.dumps({"id":str(id)})
    #     conn.request("POST", "/api/pauseScan", data, self.api_header)
    #     resp = conn.getresponse()
    #     content = resp.read()
        
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         return {"status":1}
    #     else:
    #         return {"status":0}

    # def awvs_stop_mod(self,id):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     data = json.dumps({"id":str(id)})
    #     conn.request("POST", "/api/stopScan", data, self.api_header)
    #     # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
    #     resp = conn.getresponse()
    #     content = resp.read()
        
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         return {"status":1}
    #     else:
    #         return {"status":0}


    # def awvs_del_mod(self,id):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     data = json.dumps({'id': str(id), 'deleteScanResults': 1})
    #     conn.request("POST", "/api/deleteScan", data, self.api_header)
    #     resp = conn.getresponse()
    #     content = resp.read()
    #     #{"result":"OK"}
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         return {"status":1}
    #     else:
    #         return {"status":0}


    # def awvs_getresult_mod(self,id,file_name,dirname="D:\\awvs\\"):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     data = json.dumps({"id":str(id)})
    #     conn.request("POST", "/api/getScanResults", data , self.api_header)
    #     resp = conn.getresponse()
    #     content = resp.read()

    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         try:
    #             reportid = result["data"][0]["id"].encode("gbk")
    #             conn.request("GET", "/api/download/{0}:{1}".format(id, reportid), headers=self.api_header)
    #             resp = conn.getresponse()
    #             download_contents = resp.read()
    #             #print download_contents
    #             #return {"status":1,"data":download_contents}
    #             save_file = self.download(path_file="{0}{1}.zip".format(str(dirname),str(file_name)),data=download_contents)
    #             if save_file['status'] == 1:
    #                 zipfilename = "{0}{1}.zip".format(str(dirname),str(file_name))
    #                 #print zipfilename
    #                 pdf_filename = self.unzip_dir(file_name = str(file_name),zipfilename= zipfilename)
    #                 #print pdf_filename
    #                 if pdf_filename["status"] == 1:
    #                     os.remove(zipfilename)
    #                     return {"status":1,"data":pdf_filename["data"]}
    #             else:
    #                 return {"status":2}
    #         except:
    #             return {"status":0}
    #     else:
    #         return {"status":0}


    # #this is  ok 
    # def awvs_getrisk_mod(self,id,domain):
    #     conn = httplib.HTTPConnection(self.api_url, self.api_port)
    #     conn.request("POST", "/api/getScanHistory", json.dumps({'id': str(id)}), headers=self.api_header)
    #     # conn.request("GET", "/api/listScans", headers=ACUHEADERS)
    #     resp = conn.getresponse()
    #     content = resp.read()
    #     result = json.loads(content)
    #     status = result["result"].encode("gbk")
    #     if status == "OK":
    #         content = ""
    #         for line in result["data"]:
    #             msg = line["msg"].encode("gbk")
    #             if str(domain) in msg :
    #                 arr = msg.split(",")
    #                 content = '{0}{1}{2}'.format(arr[0][-6:],arr[1],arr[2])
    #         return {"status":1,'data':content}
    #     else:
    #         return {"status":0}

    # def download(self,path_file,data):
    #     try:
    #         with open("{0}".format(path_file), "wb") as code:     
    #             code.write(data)
    #             code.close()
    #         return {"status":1,"data":path_file}
    #     except:
    #         return {"status":0}

    # def unzip_dir(self,file_name = "test",zipfilename="m:\\scan02.zip", unzipdirname="D:\\awvs\\"):
    #     fullzipfilename = os.path.abspath(zipfilename)  
    #     fullunzipdirname = os.path.abspath(unzipdirname)  
    #     #if not os.path.exists(fullzipfilename): 
    #     #print file_name,fullzipfilename

    #     #Start extract files ...
    #     result = ""
    #     try:
    #         srcZip = zipfile.ZipFile(fullzipfilename, "r")
    #         for eachfile in srcZip.namelist():
    #             #print "Unzip file %s ..." % eachfile
    #             eachfilename = os.path.normpath(os.path.join(fullunzipdirname, '{0}_{1}'.format(file_name,eachfile)))
    #             eachdirname = os.path.dirname(eachfilename)
    #             if eachfile.endswith(".pdf",4):
    #                 fd=open(eachfilename, "wb")
    #                 result = eachfilename
    #                 fd.write(srcZip.read(eachfile))
    #                 fd.close()
    #             else:
    #                 pass
    #         srcZip.close()
    #         return {"status":1,"data":result}
    #     except:
    #       return {"status":0}
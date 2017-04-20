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
import cgi  


report_save_dir = "m:\\test\\"
loginseq_dir = "C:\\Users\\Public\\Documents\\Acunetix WVS 10\\LoginSequences"

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
                            "color_white_list": ["orange", "red", "blue"],  # green,blue,orange,red四种级别
                            "bug_black_list": [                     # 漏洞黑名单，过滤掉一些危害等级高，但没什么卵用的洞
                                "User credentials are sent in clear text"
                            ]
                        }

    def parse_xml(self,file_name):
        bug_list = []

        root = minidom.parse(file_name).documentElement
        #print root.nodeName,root.nodeValue,root.nodeType
        ReportItem_list =  root.getElementsByTagName('ReportItem')
        #print root.getElementsByTagName('ScanTime')[0].firstChild.data.encode('utf-8')
        if ReportItem_list:
            for node in ReportItem_list:
                color = node.getAttribute("color")
                name = node.getElementsByTagName("Name")[0].firstChild.data.encode('utf-8')
                #print color,name
                try:
                    if color in self.filter['color_white_list'] and name not in self.filter['bug_black_list']:
                        temp = {}
                        temp['name'] = '{0}'.format(name)
                        temp['color'] = '{0}'.format(color.encode('utf-8'))
                        temp['details'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Details")[0].firstChild.data.encode('utf-8')))
                        temp['affect'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Affects")[0].firstChild.data.encode('utf-8')))
                        temp['severity'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Severity")[0].firstChild.data.encode('utf-8')))
                        temp['request'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Request")[0].firstChild.data.encode('utf-8')))
                        temp['response'] = '{0}'.format(cgi.escape(node.getElementsByTagName("Response")[0].firstChild.data.encode('utf-8')))
                        temp['repair'] = ""

                        bug_list.append(temp)
                except Exception, e:
                    pass

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



    def awvs_add(self,profile="",loginSeq="",target=""):
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


    def awvs_report(self,taskid):
        save_dir = report_save_dir
        conn = httplib.HTTPConnection(self.api_url, self.api_port)
        data = json.dumps({"id":str(taskid)})
        conn.request("POST", "/api/getScanResults", data , self.api_header)
        resp = conn.getresponse()
        content = resp.read()

        #请求下载报告
        result = json.loads(content)
        status = result["result"].encode("gbk")
        try:
            result_len = len(result["data"][0])
        except:
            result_len = 2

        #print result_len,result["data"]
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
                    #print xml_filename
                    if xml_filename["status"] == 1:
                        os.remove(zipfilename)
                        xml_data = self.parse_xml(xml_filename["data"])
                        #print xml_data
                        if xml_data['status'] == 1:
                            os.remove(xmlfilename)
                            return {"status":1,"data":xml_data["data"]}
                        else:
                            return {"status": 2}
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
        cookie_dir = loginseq_dir
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
#print AWVSTask().awvs_report(2)
#AWVSTask().unzip_dir(unzipfilename="M:\\0.zip")
#print AWVSTask().parse_xml("D:\\scan_agent\\20170412-115740.xml")
#print AWVSTask().awvs_list_loginseq()

# import HTMLParser  
  
# char = r"<script>alert(/s/)</script>"  
# t = HTMLParser.HTMLParser();  
# uChar = t.unescape(char);  
# print t,uChar,"***********"

# import cgi  
# new_cont = cgi.escape(uChar)  
# print new_cont
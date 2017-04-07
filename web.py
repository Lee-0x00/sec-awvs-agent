#-*- coding: UTF-8 -*- 
#__author__:Bing
#email:amazing_bing@outlook.com

from flask import Flask,request,redirect, url_for, render_template
from models import AWVSTask
import json


app = Flask(__name__)



node_key = "wetk2i97ssd23kjsdhu223fdv234"


@app.route("/", methods=['POST', 'GET'])
def index():
	#print request.headers.get('User-Agent')
	#request.args.items().__str__()
	result = AWVSTask().awvs_count()
	if result["status"] == 1:
		return json.dumps(result)
	else:
		return json.dumps(result)


@app.route("/add", methods=['POST', 'GET'])
def add():
	if request.method == 'POST':
		vultype = request.form.get('vultype').encode("gbk")
		loginseq = request.form.get('loginseq').encode("gbk")
		target = request.form.get('target').encode("gbk")
		#print type(vultype),type(loginseq)
		if target != "" and target.startswith("http://",0,8)  or target.startswith("https://",0,8) and vultype != type(1) and loginseq != "" :
			#多个任务，进行分割
			data = []
			if "," in target :
				try:
					content = target.split(",")
				except:
					result = {"status":0,"data":"error not offer data or format "}
					return json.dumps(result)

				for line in content:
					result = AWVSTask().awvs_add(vultype,loginseq,line)
					if result["status"] != 1:
						break
					else:
						res = {"id":result["data"],"targte":line,"status":result["status"]}
						data.append(res)
			else:
				try:
					content = target.split("\n")
				except:
					result = {"status":0,"data":"error not offer data or format "}
					return json.dumps(result)

				for line in content:
					result = AWVSTask().awvs_add(vultype,loginseq,line)
					if result["status"] != 1:
						break
					else:
						res = {"id":result["data"],"targte":line,"status":result["status"]}
						data.append(res)

			result = {"status":1,"data":data}
			return json.dumps(result)
		else:
			result = {"status":0,"data":"error not offer data or format "}
			return json.dumps(result)
	else:
		result = {"status":0,"data":"no post"}
		return json.dumps(result)


@app.route("/del", methods=['POST', 'GET'])
def delete():
	if request.method == 'POST':
		taskid = request.form.get('taskid').encode("gbk")
		if taskid != "" :
			result = AWVSTask().awvs_delete(taskid)
			return json.dumps(result)
		else:
			result = {"status":0,"data":"error not offer data or format "}
			return json.dumps(result)
	else:
		result = {"status":0,"data":"no post "}
		return json.dumps(result)


@app.route("/process", methods=['POST', 'GET'])
def process():
	if request.method == 'POST':
		taskid = request.form.get('taskid').encode("gbk")
		if taskid != "" :
			result = AWVSTask().awvs_process(taskid)
			return json.dumps(result)
		else:
			result = {"status":0,"data":"error not offer data or format "}
			return json.dumps(result)
	else:
		result = {"status":0,"data":"no post "}
		return json.dumps(result)


@app.route("/report", methods=['POST', 'GET'])
def report():
	if request.method == 'POST':
		taskid = request.form.get('taskid').encode("gbk")
		if taskid != "" :
			result = AWVSTask().awvs_report(taskid)
			return json.dumps(result)
		else:
			result = {"status":0,"data":"error not offer data or format "}
			return json.dumps(result)
	else:
		result = {"status":0,"data":"no post "}
		return json.dumps(result)

@app.route("/loginseq", methods=['POST', 'GET'])
def loginseq():
	result = AWVSTask().awvs_list_loginseq()
	if result["status"] == 1:
		return json.dumps(result)
	else:
		return json.dumps(result)


if __name__ == '__main__':
	#app.run(port=8080,debug=False)
	app.run(debug=True)










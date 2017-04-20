#-*- coding: UTF-8 -*-
#__author__:Bing
#email:amazing_bing@outlook.com

from flask import Flask,request,redirect, url_for, render_template
from models import AWVSTask
import json,os
from functools import wraps


app = Flask(__name__)


node_key = "wetk2i97ssd23kjsdhu223fdv234"

#允许访问ip地址
allowip = ['localhost','127.0.0.1']

def blocks(func):
	@wraps(func)
	def decorator(*args, **kwargs):
		remote_ip = request.remote_addr
		#return func(*args, **kwargs)
		#print remote_ip,"***********"
		if str(remote_ip) in allowip:
			#print str(remote_ip),allowip
			return func(*args, **kwargs)
		else:
			return json.dumps({"status":0,"data":"record your attack on IP!"})
	return decorator


UPLOAD_FOLDER = 'C:\\Users\\Public\\Documents\\Acunetix WVS 10\\LoginSequences'
ALLOWED_EXTENSIONS = set(['lsr'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS



@app.route('/upfile', methods = ['GET','POST'])
@blocks
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename) and ".." not in (file.filename):
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return json.dumps({"status":1})
			#redirect(url_for('upload_file', filename = filename));
		else:
			return json.dumps({"status":0})
	else:
		return json.dumps({"status":0})


@app.route("/", methods=['POST', 'GET'])
@blocks
def index():
	#print request.headers.get('User-Agent')
	#request.args.items().__str__()
	# remote_ip = request.remote_addr
	# print remote_ip,"***********",type(remote_ip)
	result = AWVSTask().awvs_count()
	if result["status"] == 1:
		return json.dumps(result)
	else:
		return json.dumps(result)


@app.route("/add", methods=['POST', 'GET'])
@blocks
def add():
	if request.method == 'POST':
		vultype = request.form.get('vultype').encode("gbk")
		loginseq = request.form.get('loginseq').encode("gbk")
		target = request.form.get('target').encode("gbk")
		#print type(vultype),type(loginseq)
		if target != "" and target.startswith("http://",0,8)  or target.startswith("https://",0,8) and vultype != "":
			#多个任务，进行分割
			data = []
			if "," in target :
				try:
					content = target.split(",")
				except:
					result = {"status":0,"data":"error not offer data or format "}
					return json.dumps(result)

				for line in content:
					result = AWVSTask().awvs_add(profile=vultype,loginSeq= "<none>",target=line)
					if result["status"] == 1:
						res = {"id":result["data"],"target":line,"status":result["status"]}
						data.append(res)
					else:
						res = {"target":line,"status":0}
						data.append(res)
			else:
				try:
					content = target.split("\n")
				except:
					result = {"status":0,"data":"error not offer data or format "}
					return json.dumps(result)

				for line in content:
					result = AWVSTask().awvs_add(profile=vultype,loginSeq= "<none>",target=line)
					if result["status"] == 1:
						res = {"id":result["data"],"target":line,"status":result["status"]}
						data.append(res)
					else:
						res = {"target":line,"status":0}
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
@blocks
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
@blocks
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
@blocks
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
@blocks
def loginseq():
	result = AWVSTask().awvs_list_loginseq()
	if result["status"] == 1:
		return json.dumps(result)
	else:
		return json.dumps(result)




if __name__ == '__main__':
	#app.run(port=8080,debug=False)
	app.run(host= "0.0.0.0",port = 8080,debug=False)










# awvs_agent
call awvs http api interface to add scan task

## Introduce
web.py:flask web api
models.py:control data operation

Interface information
API_URL|Parmerter|Return
:---:|:----:|:----:
index|null|```{"status":1,"data":task_count}``
add|vultype,loginseq,target|```{"status":1,"data":data}   data= [{"id":taskid,"target":domain,"status":status}]```
report|taskid|```{"status":1,"data":taskid}```

## Usage
1.Set the access ip in web.py
2.Set the loginseq default directory in web.py
3.Set the report directory and loginsql default directory in models.py

after then:
```
python web.py 
```


# awvs_agent    
--- 
call awvs http api interface to add scan task

## Introduce  
---
Web.py:flask web api    
Models.py:control data operation     

Interface information:      

|API_URL         | Parmerter           | Return  |
| ------------- |:-------------:| -----:|
| index     | null | ```{"status":1,"data":task_count}`` |
| add     | vultype,loginseq,target | ```{"status":1,"data":data}   data= [{"id":taskid,"target":domain,"status":status}]``` |
| report | taskid | ```{"status":1,"data":taskid}``` |
| del | taskid | ```{"status":1}``` |
| process | process | ```{"status":1,"data":process}``` |
| loginseq | null | ```{"status":1,"data":[loginseq]}``` |

## Usage   
---
1.Set the access ip in web.py     
2.Set the loginseq default directory in web.py       
3.Set the report directory and loginsql default directory in models.py    

after then:  
```
python web.py 
```

![awvs_agent](https://github.com/Canbing007/awvs_agent/blob/master/screen/1.png)
![awvs_agent](https://github.com/Canbing007/awvs_agent/blob/master/screen/2.png)
![awvs_agent](https://github.com/Canbing007/awvs_agent/blob/master/screen/3.png)
![awvs_agent](https://github.com/Canbing007/awvs_agent/blob/master/screen/4.png)
![awvs_agent](https://github.com/Canbing007/awvs_agent/blob/master/screen/5.png)

## Issue
if you have what do you need to ask me,you can give me leave a message.     
or if you have any questions,tell me by message.   



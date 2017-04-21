[![support](https://baikal.io/badges/x)](https://baikal.io/x) [![License](https://img.shields.io/:license-gpl3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/Canbing007/sec-portscan-agent)
[![python](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/e4b6f19e8a3f410f9bc70c42350ea20d/badge.svg)](https://www.quantifiedcode.com/app/project/e4b6f19e8a3f410f9bc70c42350ea20d)

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

As follow:        

#### Running agent   
![awvs_agent](https://raw.githubusercontent.com/Canbing007/awvs_agent/master/screen/1.png)

#### Add some tasks on WEB Control PlatFrom     
![awvs_agent](https://raw.githubusercontent.com/Canbing007/awvs_agent/master/screen/2.png)

#### Show tasks process and list       
![awvs_agent](https://raw.githubusercontent.com/Canbing007/awvs_agent/master/screen/3.png)

#### Show tasks report and statistics       
![awvs_agent](https://raw.githubusercontent.com/Canbing007/awvs_agent/master/screen/4.png)

#### According to a single bug report        
![awvs_agent](https://raw.githubusercontent.com/Canbing007/awvs_agent/master/screen/5.png)

## Issue
if you have what do you need to ask me,you can give me leave a message.     
or if you have any questions,tell me by message.   



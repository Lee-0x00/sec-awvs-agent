# awvs_agent
call awvs http api interface to add scan task
---

## Introduce
web.py:flask web api    
models.py:control data operation     

---
Interface information
|--API_URL--|Parmerter|Return
:---:|:----:|:----:
index|null|```{"status":1,"data":task_count}``
add|vultype,loginseq,target|
report|taskid|```{"status":1,"data":taskid}```        

|API_URL         | Parmerter           | Return  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | ```{"status":1,"data":data}   data= [{"id":taskid,"target":domain,"status":status}]``` |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

---
## Usage
1.Set the access ip in web.py     
2.Set the loginseq default directory in web.py       
3.Set the report directory and loginsql default directory in models.py    

after then:  
```
python web.py 
```


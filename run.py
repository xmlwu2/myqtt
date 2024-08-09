#! coding=utf-8
import lilo
import json
import time
import sys
import os
import random


debug=False

path,filename = os.path.split(os.path.abspath(__file__))
with open(filename+'.json','r') as f:
    ini = json.load(f)
if ini['thisid']==0:
    ini['thisid']=random.randint(20000,29999)
    with open(filename+'.json', 'w') as fw:
        json.dump(ini,fw)

srv_ip=ini['srv_ip']
runid=ini['thisid']
newid=ini['thatid']

go=True

class mycls2:
    def __init__(self,id=0,taskid=0,val=0):
        self.id=id
        self.taskid=taskid
        self.val=val
        import inspect
        self.code=inspect.getsource(self.__class__)
    def run(self):
        if debug : print('run<<<'+str(self.val)+'>>>')
        return self.val
ttt=mycls2(id=runid)

def func(sss):
    obj=lilo.dict2obj(json.loads(sss))
    if newid==0 or obj.id==newid:

        global srv_ip
        if lilo.get(id=runid,opt='-',func=func,name='task_'+str(runid)+'+',srv_ip=srv_ip)==False:
            if debug : print('get error exiting')
            return False
        if lilo.put(id=runid,opt='-',name='task_'+str(runid)+'+',srv_ip=srv_ip)==False:
            if debug : print('put error exiting')
            return False

        global go
        go=obj.go
        ttt.taskid=obj.taskid
        ttt.val=obj.run()
        return lilo.put(id=runid,name='task_'+str(runid)+'-',val=json.dumps(lilo.obj2dict(ttt)),srv_ip=srv_ip)

    else:
        return False

while go:
    getstate=False
    while not getstate:
        getstate=lilo.get(id=runid,func=func,name='task_'+str(runid)+'+',srv_ip=srv_ip)
    time.sleep(1)
    if debug : print('continue next task')
#! coding=utf-8
import lilo
import json
import time
import random
import sys
import os
import re

debug=False

path,filename = os.path.split(os.path.abspath(__file__))
with open(filename+'.json','r') as f:
    ini = json.load(f)
if ini['thisid']==0:
    ini['thisid']=random.randint(10000,19999)
    with open(filename+'.json', 'w') as fw:
        json.dump(ini,fw)

srv_ip=ini['srv_ip']
newid=ini['thisid']
runid=ini['thatid']
taskid=random.randint(1000,2000)
opt=sys.argv[1]
filename=sys.argv[2]

class mycls:
    def __init__(self,id=0,thatid=0,opt='send',taskid=0,filename='',go=True):
        self.id=id
        self.thatid=thatid
        self.taskid=taskid
        self.go=go
        self.opt=opt
        self.filename=filename.strip()
        import inspect
        self.code=inspect.getsource(self.__class__)
    def run(self):
        try:
            rrr=self.remotecode(self.opt)
        except:
            print('---@remotecode() run except!')
            return False
        else:
            return rrr
    def remotecode(self,ssss):
        srv_ip = getattr(__import__('run'), 'srv_ip')
        import lilo
        if ssss=='send':
            def fff(filename):
                lilo.get(opt='-',func=fff,id=self.thatid,type='file',name=filename,srv_ip=srv_ip)
                lilo.put(opt='-',id=self.thatid,type='file',name=filename,srv_ip=srv_ip)
                print(filename)
                return True
            ssss = lilo.get(opt='+',func=fff,id=self.thatid,type='file',name=self.filename,srv_ip=srv_ip)
        elif ssss=='recv':
            ssss = lilo.put(opt='+',id=self.thatid,type='file',name=self.filename,srv_ip=srv_ip)
        else:
            print('opt error')
            ssss = False
        return ssss


ttt=mycls(id=newid,thatid=runid,taskid=taskid,opt=opt,filename=filename,go=True)

def func(sss):
    obj=lilo.dict2obj(json.loads(sss))
    if obj.id==runid and obj.taskid==ttt.taskid:
        global srv_ip
        if lilo.get(id=newid,opt='-',func=func,name='task_'+str(runid)+'-',srv_ip=srv_ip)==False:
            if debug : print('get error exiting')
            return False
        if lilo.put(id=newid,opt='-',name='task_'+str(runid)+'-',srv_ip=srv_ip)==False:
            if debug : print('put error exiting')
            return False
        ret=obj.run()
        print(str(ret))
        return ret
    else:
        return False



def lsfunc(sss):
    ret=lilo.get(id=newid,opt='-',func=lsfunc,name='__list__',srv_ip=srv_ip)
    if not ret:
        if debug:print('<<<get error>>>')
        return False
    else:
        lss=json.loads(sss)
        vars=lss['var_names']
        for var in vars:
            st=re.search('^task_(\d+)\+$',var)
            if st:
                idvar=st.groups()[0]
                for vaar in vars:
                    st=re.search('^task_'+idvar+'-$',vaar)
                    if st:
                        if lilo.put(id=newid,opt='-',name='task_'+idvar+'+',srv_ip=srv_ip)==False:
                            if debug : print('put error exiting')
                            return False
                        if lilo.put(id=newid,opt='-',name='task_'+idvar+'-',srv_ip=srv_ip)==False:
                            if debug : print('put error exiting')
                            return False
        return True


if lilo.get(id=newid,func=lsfunc,name='__list__',srv_ip=srv_ip) and lilo.put(id=newid,opt='-',name='task_'+str(runid)+'-',srv_ip=srv_ip):
    if opt == 'send':
        if lilo.put(opt='+',id=newid,type='file',name=filename,srv_ip=srv_ip) and lilo.put(id=newid,name='task_'+str(runid)+'+',val=json.dumps(lilo.obj2dict(ttt)),srv_ip=srv_ip):
            if not lilo.get(id=newid,func=func,name='task_'+str(runid)+'-',srv_ip=srv_ip):
                if debug : print('get error end')
    elif opt == 'recv':
        if lilo.put(id=newid,name='task_'+str(runid)+'+',val=json.dumps(lilo.obj2dict(ttt)),srv_ip=srv_ip):
            if lilo.get(id=newid,func=func,name='task_'+str(runid)+'-',srv_ip=srv_ip):
                def fff(filename):
                    lilo.get(opt='-',func=fff,id=newid,type='file',name=filename,srv_ip=srv_ip)
                    lilo.put(opt='-',id=newid,type='file',name=filename,srv_ip=srv_ip)
                    print(filename)
                    return True
                if not lilo.get(opt='+',func=fff,id=newid,type='file',name=filename,srv_ip=srv_ip):
                    if debug : print('get error end')
    else:
        print('opt error')

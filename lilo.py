#! coding=utf-8
import socket
import json
import threading
import time
import os
import re


debug=True
class sock_server(object):
    def __init__(self,srv_port,timeout):
        self.server_soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.settimeout(timeout)
        self.server_soc.bind(("",srv_port))
        self.server_soc.listen(500)
 
    def __enter__(self):
        return self.server_soc
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server_soc.close()

class sock_client(object):
    def __init__(self,srv_ip,srv_port,timeout):
        self.client_soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_soc.settimeout(timeout)
        while self.client_soc.connect_ex((srv_ip,srv_port)):
            if debug:print('链接'+srv_ip+'失败')
            time.sleep(1)

    def __enter__(self):
        return self.client_soc

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_soc.close()


def srv(id=888,port=18883,timeout=10):
    global debug
    head_data= {'who'       :   'server',
                'id'        :   id,
                'timeout'   :   timeout,
                }
    vars=[]
    geters=[]
    with sock_server(port,timeout) as server:
        lasttime=0
        ii=0
        while True:
            ii=ii+1
            nowtime=time.time()
            tt=nowtime-lasttime
            if debug:print("loop time= "+str(tt)+' s')
            if debug:print('\n'+str(ii)+": start server id is "+str(id))
            lasttime=nowtime
            try:
                client_soc, client_addr = server.accept()
                client_soc.settimeout(5)
            except Exception as e:
                if debug:print(e)
            else:
                if debug:print('ip:',format(client_addr))
                try:
                    data=json.loads(client_soc.recv(1024).strip().decode("utf-8"))
                except Exception as e:
                    if debug:print(e)
                    client_soc.close()
                else:
                    if debug:print("------------"+str(data)+'=========')
                    if data['who']=='puter':
                        if data['opt']=='-' or data['size']==0:
                            if data['type']=='var':
                                existvar=False
                                badvar=None
                                for var in vars:
                                    if var['name']==data['name']:
                                        badvar=var
                                        existvar=True
                                        break
                                if existvar:
                                    vars.remove(badvar)
                                    if debug:print(str(vars))
                            elif data['type']=='file':
                                if os.path.exists(data['name']):
                                    os.remove(data['name'])
                            else:
                                if debug:print('type error')
                            client_soc.close()
                        else:
                            try:
                                total_data = b''
                                while len(total_data)<data['size']:
                                    total_data += client_soc.recv(data['size'])
                                    if debug:print('=',end='')
                                if debug:print('buf done!')
                            except Exception as e:
                                if debug:print(e)
                                client_soc.close()
                            else:
                                client_soc.close()
                                if data['type']=='var':
                                    exist=False
                                    for var in vars:
                                        if var['name']==data['name']:
                                            var['val']=total_data
                                            exist=True
                                            break
                                    if not exist:
                                        vars.append({'name':data['name'],'val':total_data})
                                elif data['type']=='file':
                                    with open(data['name'],"wb") as f:
                                        f.write(total_data)
                                else:
                                    if debug:print('type error')
                                    continue
                                bad_geters=[]
                                for geter in geters:
                                    if geter['type']==data['type'] and geter['name']==data['name']:
                                        head_data= {'who'       :   head_data['who'],
                                                    'id'        :   head_data['id'],
                                                    'timeout'   :   head_data['timeout'],
                                                    'type'      :   data['type'],
                                                    'name'      :   data['name'],
                                                    'size'      :   len(total_data)
                                                    }
                                        try:
                                            geter['sock'].sendall(json.dumps(head_data).encode("utf-8").center(1024))
                                        except Exception as e:
                                            if debug:print(e)
                                            bad_geters.append(geter)
                                        else:
                                            try:
                                                geter['sock'].sendall(total_data)
                                            except Exception as e:
                                                if debug:print(e)
                                                bad_geters.append(geter)
                                            else:
                                                if debug:print('send to '+str(geter['sock']))
                                for bad_geter in bad_geters:
                                    if bad_geter in geters:
                                        geters.remove(bad_geter)

                    elif data['who']=='geter':
                        geter= {    'sock'      :   client_soc,
                                    'id'        :   data['id'],
                                    'timeout'   :   data['timeout'],
                                    'type'      :   data['type'],
                                    'name'      :   data['name'],
                            }
                        if data['opt']=='-':
                            bad_geters=[]
                            for getit in geters:
                                if getit['id']==geter['id'] and getit['type']==geter['type'] and getit['name']==geter['name']:
                                    bad_geters.append(getit)
                            if len(bad_geters)>0:
                                for bad_geter in bad_geters:
                                    geters.remove(bad_geter)
                                if debug:print(str(geters))
                        else:
                            existgeter=False
                            for getit in geters:
                                if getit['id']==geter['id'] and getit['type']==geter['type']:
                                    getit['sock']=geter['sock']
                                    getit['name']=geter['name']
                                    getit['timeout']=geter['timeout']
                                    existgeter=True
                                    break
                            if not existgeter:
                                geters.append(geter)

                            total_data = b''
                            if data['type']=='var':
                                res=re.search('^__(.+)__$',data['name'])
                                if res:
                                    invar=res.group(1)
                                    if invar=='list':
                                        var_names=[]
                                        for var in vars:
                                            var_names.append(var['name'])
                                        files = os.listdir()
                                        gets=[]
                                        for getit in geters:
                                            gets.append({   'id'        :   getit['id'],
                                                            'type'      :   getit['type'],
                                                            'name'      :   getit['name'],
                                                        })
                                        items = {   'var_names' :   var_names,
                                                    'files'     :   files,
                                                    'geters'    :   gets
                                                }
                                        total_data=json.dumps(items).encode("utf-8")
                                else:
                                    for var in vars:
                                        if var['name']==data['name']:
                                            total_data=var['val']
                                            break
                            elif data['type']=='file':
                                if os.path.exists(data['name']):
                                    with open(data['name'],"rb") as f:
                                        total_data = f.read()
                            else:
                                if debug:print('type error')
                                client_soc.close()
                                continue
                            if len(total_data)>0:
                                head_data= {'who'       :   head_data['who'],
                                            'id'        :   head_data['id'],
                                            'timeout'   :   head_data['timeout'],
                                            'type'      :   data['type'],
                                            'name'      :   data['name'],
                                            'size'      :   len(total_data)
                                            }
                                try:
                                    client_soc.sendall(json.dumps(head_data).encode("utf-8").center(1024))
                                except Exception as e:
                                    if debug:print(e)
                                    client_soc.close()
                                else:
                                    try:
                                        client_soc.sendall(total_data)
                                    except Exception as e:
                                        if debug:print(e)
                                        client_soc.close()
                                    else:
                                        if debug:print('send to '+format(client_addr))
                    else:
                        if debug:print(str(data))
def put(opt='+',id=111,timeout=5,type='var',name='var_name',val='',srv_ip='127.0.0.1',srv_port=18883):
    head_data= {'who'       :   'puter',
                'opt'       :   opt,
                'id'        :   id,
                'timeout'   :   timeout,
                'type'      :   type,
                'name'      :   name,
                'size'      :   len(val)
                }
    total_data = b''
    if head_data['type']=='var':
        total_data=val.encode("utf-8")
    elif head_data['type']=='file':
        if os.path.exists(head_data['name']):
            with open(head_data['name'],"rb") as f:
                total_data = f.read()

    else:
        if debug:print('type error')
        return False

    head_data['size']=len(total_data)
    with sock_client(srv_ip,srv_port,timeout) as client_puter:
        try:
            client_puter.sendall(json.dumps(head_data).encode("utf-8").center(1024))
        except Exception as e:
            if debug:print(e)
            client_puter.close()
            return False
        else:
            if opt=='-' or len(total_data)==0:
                if debug:print('total_data is None or will delete obj')
                return True
            try:
                client_puter.sendall(total_data)
            except Exception as e:
                if debug:print(e)
                client_puter.close()
                return False
            else:
                if debug:print('send to '+srv_ip)
                return True

def get(opt='+',once=True,sync=True,func=None,id=000,timeout=60,type='var',name='var_name',srv_ip='127.0.0.1',srv_port=18883):
    head_data= {'who'       :   'geter',
                'id'        :   id,
                'opt'       :   opt,
                'timeout'   :   timeout,
                'type'      :   type,
                'name'      :   name,
                }
    with sock_client(srv_ip,srv_port,timeout) as client_geter:
        try:
            client_geter.sendall(json.dumps(head_data).encode("utf-8").center(1024))
        except Exception as e:
            if debug:print(e)
            client_geter.close()
            return False
        else:
            if opt=='-':
                if debug:print('will delete geter!')
                return True
            while True:
                try:
                    data=json.loads(client_geter.recv(1024).strip().decode("utf-8"))
                except Exception as e:
                    if debug:print(e)
                    client_geter.close()
                    return False
                else:
                    if data['who']=='server':
                        try:
                            total_data = b''
                            while len(total_data)<data['size']:
                                total_data += client_geter.recv(data['size'])
                                if debug:print('=',end='')
                            if debug:print('buf done!')
                        except Exception as e:
                            if debug:print(e)
                            client_geter.close()
                            return False
                        else:
                            if data['type']=='var':
                                val=total_data.decode("utf-8")
                                if func:
                                    if sync:
                                        return func(val)
                                    else:
                                        threading.Thread(target=func, args=(val,)).start()
                                else:
                                    if debug:print(val)
                            elif data['type']=='file':
                                with open(data['name'],"wb") as f:
                                    f.write(total_data)
                                if func:
                                    if sync:
                                        return func(data['name'])
                                    else:
                                        threading.Thread(target=func, args=(data['name'],)).start()
                                else:
                                    if debug:print(data['name'] + ' download finish. len is:' + str(data['size']))
                            else:
                                if debug:print('type error')
                            if once:
                                break
    return True

def obj2dict(obj):
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d

def dict2obj(d):
    if 'code' in d:
        code=d.pop('code').replace('import inspect','').replace('self.code=inspect.getsource(self.__class__)','')
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        exec(code,globals())
        module = __import__('lilo')
        class_ = getattr(module, class_name)
        args = dict((key, value) for key, value in d.items())
        instance = class_(**args)
    elif '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key, value) for key, value in d.items())
        instance = class_(**args)
    else:
        instance = d
    return instance
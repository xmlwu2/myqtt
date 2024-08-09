#! coding=utf-8
import lilo
import json
import time
import random
import sys
import os
import re

debug=True

html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript" src="http://api.map.baidu.com/api?ak=7RtxfdKlPSLSQkG0Trh138VbzF2ifPkd&v=2.0"></script>
</head>
<body>
  <div style="width:800px;height:600px;border:#ccc solid 1px;" id="dituContent"></div>
</body>
<script type="text/javascript">
var xy=[];
createMap();//创建地图图
    function translateCallback(data){
      if(data.status === 0) {
        var marker = new BMap.Marker(data.points[0]);
        map.addOverlay(marker);
        var label = new BMap.Label("here",{offset:new BMap.Size(20,-10)});
        marker.setLabel(label); //添加百度label
        map.setCenter(data.points[0]);
		map.centerAndZoom(data.points[0],17);//设定地图的中心点和坐标并将地图显示在地图容器中
      }
    }
    function createMap(){//创建地图函数：
        var map = new BMap.Map("dituContent");//在百度地图容器中创建一个地图
        window.map = map;//将map变量存储在全局
		setTimeout(function(){
			var pointArr = [];
			pointArr.push(new BMap.Point(xy[0], xy[1]));
			var convertor = new BMap.Convertor();
			convertor.translate(pointArr, 1, 5, translateCallback)
		}, 500);
        map.enableScrollWheelZoom();//启用地图滚轮放大缩小
        map.enableKeyboard();//启用键盘上下左右键移动地图
		var ctrl_nav = new BMap.NavigationControl({anchor:BMAP_ANCHOR_TOP_LEFT,type:BMAP_NAVIGATION_CONTROL_LARGE});//向地图中添加缩放控件
		map.addControl(ctrl_nav);
		var ctrl_sca = new BMap.ScaleControl({anchor:BMAP_ANCHOR_BOTTOM_LEFT});//向地图中添加比例尺控件
		map.addControl(ctrl_sca);
		var ctrl_ove = new BMap.OverviewMapControl({anchor:BMAP_ANCHOR_BOTTOM_RIGHT,isOpen:1});//向地图中添加缩略图控件
		map.addControl(ctrl_ove);
    }
</script>
</html>
"""


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
filename='安安安安安.xlsx'

class mycls:
    def __init__(self,id=0,thatid=0,ss='',taskid=0,filename='',go=True):
        self.id=id
        self.thatid=thatid
        self.taskid=taskid
        self.go=go
        self.ss=ss
        self.filename=filename.strip()
        # import re
        # st=re.search('\"(.+)\"',self.ss)
        # if st:
            # self.ss=st.groups()[0]
        import inspect
        self.code=inspect.getsource(self.__class__)
    def run(self):
        print(str(self.ss))
        try:
            rrr=self.remotecode(self.ss)
        except:
            self.ss=self.ss+'---@remotecode() run except!'
        else:
            self.ss=rrr
        return self.ss
    def remotecode(self,ssss):
        if self.thatid==21879:
            my_clock = getattr(__import__('__main__'), 'my_clock')
            NeoPixel = getattr(__import__('__main__'), 'NeoPixel')
            from random import randint
            import time
            def func():
                for i in range(60):
                    my_clock.np.fill(my_clock.Black)
                    for j in range(27):
                        my_clock.pix(randint(0,my_clock.num-1),NeoPixel.wheel(randint(0,255)))
                    my_clock.np.write()
                    time.sleep_ms(100)
            import _thread
            _thread.start_new_thread(func,())
            #func()
        elif self.thatid==26495:
            my_clock = getattr(__import__('__main__'), 'my_clock')
            oldss=my_clock.ss
            my_clock.ss=ssss
            ssss=oldss
        elif self.thatid==20196:
            machine = getattr(__import__('__main__'), 'machine')
            my_clock = getattr(__import__('__main__'), 'my_clock')
            NeoPixel = getattr(__import__('__main__'), 'NeoPixel')
            _thread = getattr(__import__('__main__'), '_thread')
            randint = getattr(__import__('__main__'), 'randint')
            time = getattr(__import__('__main__'), 'time')
            def func():
                for j in range(10):
                    for i in range(10):
                        my_clock.pix(randint(0,my_clock.num-1),NeoPixel.wheel(randint(0,255)))
                    my_clock.np.write()
                    time.sleep_ms(500)
            _thread.start_new_thread(func,())
            #func()
            ssss=machine.RTC().datetime()
        elif self.thatid==23046:
            # http://www.mithril.com.au/android/doc/LocationFacade.html
            import time
            import androidhelper
            droid = androidhelper.Android()
            droid.startLocating()
            time.sleep(15)
            loc = droid.readLocation().result
            #if loc == {}:
                #loc = droid.getLastKnownLocation().result
            if loc != {}:
                try:
                    n = loc['gps']
                except KeyError:
                    n = loc['network'] 
                if n != None:
                    la,lo= n['latitude'],n['longitude']
                    print(str((lo,la)))
                    ssss=(lo,la)
                else:
                    ssss=False
            else:
                ssss=False
            droid.stopLocating()
        else:
            import os
            ssss=''.join(os.popen(ssss).readlines())

        return ssss


ttt=mycls(id=newid,thatid=runid,taskid=taskid,ss=''.join(sys.stdin.readlines()),filename=filename,go=True)

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
        if ret and ttt.thatid==23046:
            global html
            try:
                with open('xy.html', 'w') as fw:
                    fw.write(html.replace('var xy=[];','var xy='+ str(ret) +';'))
            except:
                if debug : print('write xy.html error')
            else:
                os.startfile('xy.html')

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
        print(sss)
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


if lilo.get(id=newid,func=lsfunc,name='__list__',srv_ip=srv_ip):
    if lilo.put(id=newid,opt='-',name='task_'+str(runid)+'-',srv_ip=srv_ip):
        if lilo.put(id=newid,name='task_'+str(runid)+'+',val=json.dumps(lilo.obj2dict(ttt)),srv_ip=srv_ip):
            lilo.get(timeout=60,id=newid,func=func,name='task_'+str(runid)+'-',srv_ip=srv_ip)

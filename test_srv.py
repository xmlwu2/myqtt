import lilo
import time
from multiprocessing import Process


class MyProcess(Process):
    def run(self):
        print("lilo.srv子进程开始.")
        lilo.srv()


if __name__ == '__main__':
    while True:
        p = MyProcess()
        p.start()
        while True:
            time.sleep(60)
            def lsfunc(sss):
                print(sss)
                return True
            ret=lilo.get(timeout=10,id=666,func=lsfunc,name='__list__',srv_ip='127.0.0.1')
            if not ret:
                while p.is_alive():
                    print("is_alive will terminate")
                    p.terminate()
                    time.sleep(1)
                break



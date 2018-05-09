# -*- coding: utf-8 -*-
__author__ = 'qutoutiao'

import time
import subprocess
import sched


schedule = sched.scheduler(time.time, time.sleep)


def func():

    lsit = ["scrapy crawl toutiao"]
    for i in lsit:
        p = subprocess.Popen(i)
        if p.wait() == 0:
            print(i+"kill")
            p.kill()


def perform1(inc):
    #   加入调度时间schedule.enter(x1,x2,x3,x4)，
    #   参数意义：间隔事件；优先级（同时到达的两个时间同时执行是定序）；被调用触发的函数；给他的参数
    #   注意最后一个参数：一定要以tuple给,如果只有一个参数就(xx,)
    schedule.enter(inc, 0, perform1, (inc,))
    #   周期执行的函数
    func()


def mymain():
    schedule.enter(0, 0, perform1, (1800,))


def get_name(argv):

    try:
        # global SERVER
        # SERVER = argv[0:][0]
        return argv[0:][0]

    except:

        return None


#   __name__是当前模块名，当模块被运行时模块名为__main__
#   即：当模块被直接运行时，以下代码块将被运行，当模块被导入是，代码块不被运行
if __name__ == "__main__":
    # global SERVER
    # SERVER = get_name(sys.argv[1:])
    mymain()
    schedule.run()



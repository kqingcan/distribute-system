import time, sys, queue,random
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()


def re_task_queue():
    global task_queue
    return task_queue


def re_result_queue():
    global result_queue
    return result_queue


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')


def register(server_addr, port, authkey):
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task_queue', callable=re_task_queue)
    QueueManager.register('get_result_queue', callable=re_result_queue)
    manager = QueueManager(address=(server_addr, port), authkey=authkey)
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    return task, result


def connect(server_addr, port, authkey):
    manager =QueueManager(address=(server_addr, port), authkey=authkey)
    manager.connect()
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    return task, result

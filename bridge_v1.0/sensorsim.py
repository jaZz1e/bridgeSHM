import threading
import socket
import time
import random

class Sensor(threading.Thread):
    def __init__(self,f_sample,s_type,s_name,socket_id,num):
        threading.Thread.__init__(self)
        self.fs = f_sample
        self.stype = s_type
        self.sname = s_name
        self.sid = socket_id
        self.num = num
    def run(self):
        while True:
            svalue = round(random.random()*10+self.num*10,2)
            self.sid.send((str(self.stype)+'%02d' % self.sname+'\t'+str(svalue).rjust(5)+str('\n')).encode('utf-8'))
            
            time.sleep(1/self.fs)

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('localhost',9090))

    acc_num = 10
    tmp_num = 2

    acc_fs = 1
    tmp_fs = 2

    sensor_list = []
    for i in range(acc_num):
        acc_sensor = Sensor(acc_fs,'A',i,client,i)
        sensor_list.append(acc_sensor)

    for i in range(tmp_num):
        tmp_sensor = Sensor(tmp_fs,'T',i,client,i)
        sensor_list.append(tmp_sensor)

    for sensor in sensor_list:
        sensor.start()
    for sensor in sensor_list:
        sensor.join()
        

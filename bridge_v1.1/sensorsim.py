import threading
import socket
import time
import random
import numpy as np

class Sensor_model(threading.Thread):
    def __init__(self,fs,bridge_id,sensor_type,sensor_globalnum,socket_id):
        threading.Thread.__init__(self)
        self.fs = fs
        self.bridge_id = bridge_id
        self.stype = sensor_type
        self.glbnum = sensor_globalnum
        self.socket_id = socket_id

    def run(self):
        t = 0
        while True:
            data_content = np.sin(2*np.pi*t)+0.5*random.random()
            # print(t,data_content)
            data_content = round(data_content,5)
            #print(data_content)
            t = t+0.1
            # data_content = round(random.random(),2)
            self.socket_id.send((self.bridge_id+ '\t' + str('%03d' % self.glbnum) + '\t' + str(data_content).rjust(10) + str('\n')).encode('utf-8'))
            time.sleep(1/self.fs)


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('localhost',9050))

    strain_num = 55
    strian_fs = 1
    crack_num = 33
    crack_fs = 1
    sensor_list = []

    num_cnt = 1

    #拉林河大桥应变
    for i in range(strain_num):
        strain_sensor = Sensor_model(strian_fs,'LLH','strain',num_cnt,client)
        sensor_list.append(strain_sensor)
        num_cnt += 1

    for i in range(crack_num):
        crack_sensor = Sensor_model(crack_fs,'LLH','crack',num_cnt,client)
        sensor_list.append(crack_sensor)
        num_cnt += 1
        
    tmp_sensor = Sensor_model(0.1,'LLH','tmp',0,client)

    for sensor in sensor_list:
        sensor.start()
    tmp_sensor.start()

    for sensor in sensor_list:
        sensor.join()

    tmp_sensor.join()
    

 

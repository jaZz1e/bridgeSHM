import threading
import socket
import time
import random

class Sensor_model(threading.Thread):
    def __init__(self,fs,bridge_id,sensor_type,sensor_globalnum,socket_id):
        threading.Thread.__init__(self)
        self.fs = fs
        self.bridge_id = bridge_id
        self.stype = sensor_type
        self.glbnum = sensor_globalnum
        self.socket_id = socket_id

    def run(self):
        while True:
            data_content = round(random.random(),2)
            self.socket_id.send((self.bridge_id+ '\t' + str('%03d' % self.glbnum) + '\t' + str(data_content).rjust(5) + str('\n')).encode('utf-8'))
            time.sleep(1/self.fs)


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('localhost',9080))

    strain_num = 55
    strian_fs = 10
    sensor_list = []

    num_cnt = 1

    #拉林河大桥应变
    for i in range(strain_num):
        strain_num = Sensor_model(strian_fs,'LLH','strain',num_cnt,client)
        sensor_list.append(strain_num)
        num_cnt += 1

    for sensor in sensor_list:
        sensor.start()

    for sensor in sensor_list:
        sensor.join()

 

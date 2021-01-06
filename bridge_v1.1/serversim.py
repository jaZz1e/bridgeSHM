import socket
import queue
import threading
import MySQLdb
import time

#拉林河：1
#通河：2

bridge_map = {'LLH':1,'THQ':2}

class DDThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not q_exe.empty():
                data_st = q_exe.get()
                s_name,val = data_st.split()
                cursor.execute('INSERT INTO `%s` VALUES (\'%s\' , now());'%(s_name,val))
                

                cursor.execute(cmd)
                con.commit()

class DBThread(threading.Thread):
    def __init__(self,bridgename):
        threading.Thread.__init__(self)
        self.bridgeid = bridge_map[bridgename]
        self.bridgename = bridgename

    def run(self):
        while True:
            if not queue_list[self.bridgeid-1].empty():
                data_st = queue_list[self.bridgeid-1].get()
                print(data_st)
                bdname, num, val = data_st.split()

                cur_date = time.strftime('%Y%m%d',time.localtime())
                tbname = self.bridgename + str(num) + cur_date
                cmd = "SELECT table_name FROM information_schema.TABLES WHERE table_name ='%s';" % (tbname)
                # print(cmd)
                cursor.execute(cmd)
                con.commit()

                if not len(cursor.fetchall()):
                    cmd = "CREATE TABLE `%s` (`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,`val` VARCHAR(10) NOT NULL,`nowtime` DATETIME NOT NULL);" % (tbname)
                    cursor.execute(cmd)
                    con.commit()

                    cursor.execute("INSERT INTO `%s` (`val`,`nowtime`) VALUE ('%s' , now());"%(tbname,val))
                    con.commit()

                else:
                    cursor.execute("INSERT INTO `%s` (`val`,`nowtime`) VALUE ('%s' , now());"%(tbname,val))
                    con.commit()

def get_conn():
    con = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='9qqhaoma',
        db='BridgeSHM',
        charset='utf8'
    )
    return con

if __name__ == '__main__':

    con = get_conn()
    cursor = con.cursor()
    cursor.execute('USE `BridgeSHM`;')

    queue_list = []
    q_LLH = queue.Queue()
    queue_list.append(q_LLH)
    q_TH = queue.Queue()
    queue_list.append(q_TH)

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',9050))
    server.listen(5)

    dbthread = DBThread('LLH')
    dbthread.start()

    while True:
        print('wait client')
        conn, addr = server.accept()
        while True:
            try:
                data = conn.recv(19)
                data = data.decode()
                bridge_id = bridge_map[data.split()[0]]
                queue_list[bridge_id-1].put(data)
                # print(bridge_id)
                # print(data)
            except:
                break
        conn.close()
    con.close()


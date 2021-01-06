import socket
import queue
import threading
import MySQLdb

class DDThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not q_exe.empty():
                data_st = q_exe.get()
                s_name,val = data_st.split()
                #cursor.execute('INSERT INTO `%s` VALUES (\'%s\' , now());'%(s_name,val))
                cmd = "INSERT INTO `%s` (`val`,`nowtime`) VALUE ('%s' , now());"%(s_name,val)
                #print(cmd)
                cursor.execute(cmd)
                con.commit()

def get_conn():
    con = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='9qqhaoma',
        db='sensors',
        charset='utf8'
    )
    return con

con = get_conn()
cursor = con.cursor()
cursor.execute('SHOW TABLES;')
#cursor.execute('USE `sensors`;')
print(cursor.fetchall())

q_exe = queue.Queue()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',9090))
server.listen(5)

dthread = DDThread()
dthread.start()

while True:
    conn,addr = server.accept()
    while True:
        data = conn.recv(10)
        q_exe.put(data.decode())
        #print(data.decode())
    conn.close()

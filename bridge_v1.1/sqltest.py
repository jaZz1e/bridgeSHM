import MySQLdb


# SELECT table_name FROM information_schema.TABLES WHERE table_name ='a01';

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

try:
	con = get_conn()
	cursor = con.cursor()
	cursor.execute('USE `sensors`;')
	print('suc')
except:
	print('error')

cmd = "SELECT table_name FROM information_schema.TABLES WHERE table_name ='a01';"
#print(cmd)
cursor.execute(cmd)
con.commit()

print(len(cursor.fetchall()))


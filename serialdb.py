import MySQLdb

def connect(h,u,p,db,u_s):
	return MySQLdb.connect(host=h, # your host, usually localhost
					user=u, # your username
					passwd=p, # your password
					db=db,
					unix_socket=u_s) # name of the data base

def cursor(conn):
	return conn.cursor()

def save(conn,cursor,bytes):
	cursor.execute('INSERT INTO  `reads` (  `value` ) VALUES ( %s )', bytes)
	conn.commit()

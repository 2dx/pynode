#!/user/bin/env python
# -*- coding: utf-8 -*-

from . import crypto
from . import const

import sqlite3
conn = sqlite3.connect(const.NODE.SQLITE_PATH)

c = conn.cursor()

for tablename in ["preprepare","prepare","pool","transactions","nodes","certs"]:
	try:
		c.execute('DROP TABLE {}'.format(tablename))
	except:
		pass

# Create table
c.execute('''CREATE TABLE preprepare
             (nodePublicKey text unique, data text, created integer)''')

c.execute('''CREATE TABLE prepare
             (nodePublicKey text unique, data text, created integer)''')

c.execute('''CREATE TABLE pool
             (data text unique, signature text, deadline integer)''')

c.execute('''CREATE TABLE transactions
             (txid text unique, data text)''')
# txid --> アドレス_ブロック高_番号

c.execute('''CREATE TABLE nodes
             (endpoint text, publicKey text, address text unique, balance integer, lastChecked integer)''')

c.execute('''CREATE TABLE certs
             (id text unique, data text)''')

# # Insert a row of data
# c.execute("INSERT INTO preprepare VALUES (222,222,3)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


def insert(tablename, insertdata):
	conn = sqlite3.connect(const.NODE.SQLITE_PATH)
	try:
		sql = "INSERT INTO "+tablename+" VALUES (?" + ',?'*(len(insertdata)-1) + ")"
		with conn:
			conn.execute(sql, insertdata)
	except sqlite3.IntegrityError:
		pass

def accountSearch(address):
	conn = sqlite3.connect(const.NODE.SQLITE_PATH)
	cur = conn.cursor()
	cur.execute('SELECT * FROM transactions WHERE txid LIKE ?', ('{}%'.format(address),))
	return cur.fetchall()

def dataSearch(tablename, dataToSearch):
	return search(tablename, "data", dataToSearch)

def search(tablename, columnName, dataToSearch):
	conn = sqlite3.connect(const.NODE.SQLITE_PATH)
	cur = conn.cursor()
	cur.execute('SELECT * FROM '+tablename+' WHERE '+columnName+' = ?', ('{}'.format(dataToSearch),))
	return cur.fetchall()

def fetchAll(tablename):
	conn = sqlite3.connect(const.NODE.SQLITE_PATH)
	cur = conn.cursor()
	cur.execute('SELECT * FROM '+tablename)
	return cur.fetchall()

def update(tablename, key, value, dict):
	# already exist?
	conn = sqlite3.connect(const.NODE.SQLITE_PATH)
	cur = conn.cursor()
	cur.execute("SELECT * FROM "+tablename+" WHERE "+key+" = ?", ('{}'.format(value),))
	res = cur.fetchall()
	# print(res)
	if len(res) > 0:
		# print(dict)
		keys = dict.keys()
		s = ""
		for k in keys:
			s += k+"=:"+k+", "
		s = s[:-2]
		sql = "UPDATE "+tablename+" set "+s+" where {}=:{}".format(key,key)
		# print(sql)
		dict.update({key:value})
		with conn:
			conn.execute(sql,dict)
		return True
	else:
		return False
	
def delete(tablename, key, value):
	conn = sqlite3.connect(const.NODE.SQLITE_PATH)
	sql = "DELETE from "+tablename+" where {}=:{}".format(key,key)
	with conn:
		conn.execute(sql,{key:value})
	return True
	






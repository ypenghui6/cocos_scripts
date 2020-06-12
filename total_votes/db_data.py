# -*- coding:utf-8 -*-

import sqlite3    
import os

def get_connect():
	path = os.getcwd()

	path_ = path + '\\' + 'db.db'
	print(path_)
	conn = sqlite3.connect(path_) 
	cur = conn.cursor()
	return conn, cur


def init_tables():
	'''
	表一  账户表
	account_id 账户 总得票数  时间  是否是db或委员

	表二 支持者表
	id   account_id   支持者  支持票数  时间

	表三 账户&支持者表
	id   账户 总得票数   是否是db或委员  支持者  支持票数  时间

	表四  1天投票变化表
	id   account_id  账户 总得票数  支持者_today   支持票数_today   支持者_yestoday  支持票数_yestoday 时间

	表五  总投票数
	id   总得票数  committeees_total_votes   committeees_supporters_real_votes   witnesses_total_votes  witnesses_supporters_real_votes 时间
	'''	
	conn,cur = get_connect()
	account_sql = 'create table if not exists account (id integer primary key , account varchar(20) NOT NULL , scores integer , time varchar(20) NOT NULL , type integer )'
	account_supports_sql = 'create table if not exists account_supports (id integer primary key , account varchar(20) NOT NULL , scores integer , type integer, support varchar(20) NOT NULL , support_scores integer , time varchar(20) NOT NULL )'
	supports_sql = 'create table if not exists supports (id integer primary key , account_id id integer, support varchar(20) NOT NULL , scores integer , time varchar(20) NOT NULL )'
	supports_analysis_sql = 'create table if not exists supports_analysis (id integer primary key , account_id id integer, account varchar(20) NOT NULL , scores integer , support_t varchar(20) NOT NULL , \
	support_scores_t integer , support_y varchar(20) NOT NULL , support_scores_y integer ,time varchar(20) NOT NULL ) '
	total_votes_sql = 'create table if not exists total_votes (id integer primary key , scores integer , committeees_total_votes integer, committeees_supporters_real_votes integer , witnesses_total_votes integer , witnesses_supporters_real_votes integer , time varchar(20) NOT NULL )'
	cur.execute(account_sql) 
	cur.execute(account_supports_sql) 
	cur.execute(supports_sql)
	cur.execute(supports_analysis_sql)
	cur.execute(total_votes_sql)
	conn.commit()

def update_data(_table, _data):
	conn,cur = get_connect()
	sql = ""
	if _table == "account":
		if len(_data) < 5:
			print("Error data, the number of parameters g is less than 5")
			return -1
		sql = 'insert into account values(?,?,?,?,?)'
		cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4],)) 
	elif _table == "supports":
		if len(_data) < 5:
			print("Error data, the number of parameters g is less than 5")
			return -1
		sql = 'insert into supports values(?,?,?,?,?)'
		cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4],)) 
	elif _table == "account_supports":
		if len(_data) < 7:
			print("Error data, the number of parameters g is less than 7")
			return -1
		sql = 'insert into account_supports values(?,?,?,?,?,?,?)'
		cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4], _data[5], _data[6],)) 
	elif _table == "total_votes":
		if len(_data) < 7:
			print("Error data, the number of parameters g is less than 7")
			return -1
		sql = 'insert into total_votes values(?,?,?,?,?,?,?)'
		cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4], _data[5], _data[6],)) 		
	elif _table == "supports_analysis":		
		if len(_data) < 9:
			print("Error data, the number of parameters g is less than 5")
			return -1		
		sql = 'insert into supports values(?,?,?,?,?,?,?,?,?)'
		cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4], _data[5], _data[6], _data[7], _data[8],)) 
	else:
		print("unkown table...")
		return -1	
	conn.commit()
	cur.close() 
	conn.close() 
	print('success update data...')


def select_tables():
	cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables=cur.fetchall()
	print(tables)
	return tables
''' 
执行 select_data()

[('numbers',)]
''' 

def select_data_with_time(_table, _time):
	conn,cur = get_connect()
	sql = "SELECT * from " + _table + " where time=?;"
	cur.execute(sql,(_time,)) 
	data_all = cur.fetchall()
	cur.close() 
	conn.close() 
	a = len(data_all)
	print('共有 '+ str(a) + ' 条记录')
	return data_all


# init_tables()
table="account"
data=[3,"tom",10000,"2020-05-19",0]
# update_data(table, data)
data=select_data_with_time("account", "2020-05-19")	
print(data)

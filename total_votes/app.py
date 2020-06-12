#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import threading

import datetime

import json
import requests
import os
import socket
from multiprocessing import Process
import sqlite3    

from http.server import HTTPServer, BaseHTTPRequestHandler

import sys
import hashlib

QUIT = 0
FILE_NAME = '/index.html'
#DAY = 24*60*60
DAY = 1
IS_UPDATE_TODAY = ""
#cli_wallet_url = "http://api.cocosbcx.net"
headers = {"content-type": "application/json"}
#chain_api_url = "https://test.cocosbcx.net"  
chain_api_url = "https://api.cocosbcx.net"  

FILE_LOCK = '/lock'
account_names = {}

def wite_lock():
    path = os.getcwd()
    path = path + FILE_LOCK
    f = open(path, mode='a')
    f.writelines('\n')
    f.writelines(datetime.datetime.now().strftime("%Y-%m-%d"))
    f.close()

def read_lock():
    path = os.getcwd()
    path = path + FILE_LOCK
    result = "open file failed"
    try:
        f = open(path, mode='r')
        lines = f.readlines()
        result = lines[-1]
        f.close()
        return result.decode()
    except Exception as e:
        return result


def get_connect():
    path = os.getcwd()
    path_ = path + '/' + 'db.db'
    conn = sqlite3.connect(path_) 
    cur = conn.cursor()
    return conn, cur


def init_tables():
    '''
    表一  账户表
    account_id 总得票数  时间  是否是db或委员

    表二 支持者表
    account_id   支持者id  支持票数  时间

    表三 账户&支持者表
    account_id 总得票数   是否是db或委员  支持者id  支持票数  时间

    表四  N天投票变化表
    account_id 是否是db或委员 总得票数  支持者_today   支持票数_today   支持者_history  支持票数变动_history 时间

    表五  总投票数
    总得票数  committeees_total_votes   committeees_supporters_real_votes   witnesses_total_votes  witnesses_supporters_real_votes 时间
    ''' 
    conn,cur = get_connect()
    account_sql = 'create table if not exists account (id integer primary key autoincrement, time varchar(20) NOT NULL , account_id varchar(20) NOT NULL , scores varchar(20) , type integer, account_real_id varchar(20) NOT NULL )'
    # account_supports_sql = 'create table if not exists account_supports (id integer primary key autoincrement, time varchar(20) NOT NULL , account_id varchar(20) NOT NULL , scores varchar(20) , type integer, \
    #  support_id varchar(20) NOT NULL , support_scores varchar(20) )'
    supports_sql = 'create table if not exists supports (id integer primary key autoincrement, time varchar(20) NOT NULL , account_id varchar(20) NOT NULL , support_id varchar(20) NOT NULL , scores varchar(20) )'
   
    supports_analysis_sql = 'create table if not exists supports_analysis (id integer primary key autoincrement, time varchar(20), account_id varchar(20) NOT NULL , support_id varchar(20) NOT NULL ,\
     type integer, scores varchar(20) , support_scores_t varchar(20) , support_scores_history varchar(20), account_real_id varchar(20) NOT NULL ) '
   
    total_votes_sql = 'create table if not exists total_votes (id integer primary key autoincrement, time varchar(20) NOT NULL , scores varchar(20) , committeees_total_votes varchar(20), committeees_supporters_real_votes varchar(20) , \
     witnesses_total_votes varchar(20) , witnesses_supporters_real_votes varchar(20) )'
   
    account_name_sql = 'create table if not exists account_name (id integer primary key autoincrement, account_real_id varchar(20) NOT NULL, name varchar(20) NOT NULL)'

    cur.execute(account_sql) 
    # cur.execute(account_supports_sql) 
    cur.execute(supports_sql)
    cur.execute(supports_analysis_sql)
    cur.execute(total_votes_sql)
    cur.execute(account_name_sql)
    conn.commit()

def update_data(_table, _data):
    str_lock = read_lock()
    if str_lock == datetime.datetime.now().strftime("%Y-%m-%d"):
        return
    conn,cur = get_connect()
    check_data = []
    if _table == "account":
        check_data = select_data_with_time_id(_table, datetime.datetime.now().strftime("%Y-%m-%d"), _data[2])
    elif _table == "supports":
        check_data = select_data_with_ids(_table, datetime.datetime.now().strftime("%Y-%m-%d"), _data[2], _data[3])               
    elif _table == "supports_analysis":
        check_data = select_data_with_ids(_table, datetime.datetime.now().strftime("%Y-%m-%d"), _data[1], _data[2])     
    elif _table == "account_name":
        check_data = select_data_with_id(_table, _data[0])               
    else:
        check_data = select_data_with_time(_table, datetime.datetime.now().strftime("%Y-%m-%d"))
    if(len(check_data)):
        return 0

    sql = ""
    if _table == "account":
        if len(_data) < 5:
            print("Error data, the number of parameters g is less than 6")
            return 0
        sql = 'insert into account values(NULL,?,?,?,?,?)'
        cur.execute(sql, (_data[0], _data[1], _data[2], _data[3],_data[4],)) 
    elif _table == "supports":
        if len(_data) < 4:
            print("Error data, the number of parameters g is less than 4")
            return 0
        sql = 'insert into supports values(NULL,?,?,?,?)'
        cur.execute(sql, (_data[0], _data[1], _data[2], _data[3],)) 
    # elif _table == "account_supports":
    #     if len(_data) < 6:
    #         print("Error data, the number of parameters g is less than 6")
    #         return 0
    #     sql = 'insert into account_supports values(NULL,?,?,?,?,?,?)'
    #     cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4], _data[5],)) 
    elif _table == "total_votes":
        if len(_data) < 6:
            print("Error data, the number of parameters g is less than 6")
            return 0
        sql = 'insert into total_votes values(NULL,?,?,?,?,?,?)'
        cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4], _data[5],))       
    elif _table == "supports_analysis":     
        if len(_data) < 8:
            print("Error data, the number of parameters g is less than 7")
            return -1       
        sql = 'insert into supports_analysis values(NULL,?,?,?,?,?,?,?,?)'
        cur.execute(sql, (_data[0], _data[1], _data[2], _data[3], _data[4], _data[5], _data[6], _data[7],)) 
    elif _table == "account_name":     
        if len(_data) < 2:
            print("Error data, the number of parameters g is less than 2")
            return -1       
        sql = 'insert into account_name values(NULL,?,?)'
        cur.execute(sql, (_data[0], _data[1],))         
    else:
        print("unkown table...")
        return 0   
    conn.commit()
    cur.close() 
    conn.close() 
    print('success update data...')
    return 1


def delete_datas(_table,_time):
    if _table != "account_name":
        conn,cur = get_connect()
        sql = 'DELETE from ' + _table + ' where time=? ;'
        cur.execute(sql,(_time,)) 
        conn.commit()
        cur.close() 
        conn.close() 
    return 1

def select_tables():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=cur.fetchall()
    print(tables)
    return tables
''' 
执行 select_data()

[('numbers',)]
''' 
def select_all_data(_table):
    conn,cur = get_connect()
    sql = "SELECT * from " + _table + ";"
    cur.execute(sql) 
    data_all = cur.fetchall()
    cur.close() 
    conn.close() 
    a = len(data_all)
    print('共有 '+ str(a) + ' 条记录')
    return data_all

def select_data_with_id(_table, account_real_id):
    conn,cur = get_connect()
    sql = "SELECT * from " + _table + " where account_real_id=? ;"
    cur.execute(sql,(account_real_id,)) 
    data_all = cur.fetchall()
    cur.close() 
    conn.close() 
    a = len(data_all)
    print('共有 '+ str(a) + ' 条记录')
    return data_all

def select_data_with_time_type(_table, _time, _type_or_id):
    conn,cur = get_connect()
    sql = ""
    if _table == "supports" and (_type_or_id != 0 or _type_or_id != 1):
        sql = "SELECT * from " + _table + " where time=? AND account_id=? ;"
    else :
        sql = "SELECT * from " + _table + " where time=? AND type=? ;"
    cur.execute(sql,(_time,_type_or_id,)) 
    data_all = cur.fetchall()
    cur.close() 
    conn.close() 
    a = len(data_all)
    print('共有 '+ str(a) + ' 条记录')
    return data_all

def select_data_with_time_id(_table, _time, account_id):
    conn,cur = get_connect()
    sql = "SELECT * from " + _table + " where time=? AND account_id=? ;"
    cur.execute(sql,(_time,account_id,)) 
    data_all = cur.fetchall()
    cur.close() 
    conn.close() 
    a = len(data_all)
    print('共有 '+ str(a) + ' 条记录')
    return data_all

def select_data_with_time(_table, _time):
    conn,cur = get_connect()
    sql = "SELECT * from " + _table + " where time=? ;"
    cur.execute(sql,(_time,)) 
    data_all = cur.fetchall()
    cur.close() 
    conn.close() 
    a = len(data_all)
    print('共有 '+ str(a) + ' 条记录')
    return data_all
    

def select_data_with_ids(_table, _time, account_id, support_id):
    conn,cur = get_connect()
    sql = "SELECT * from " + _table + " where time=? AND account_id=? AND support_id=? ;"
    cur.execute(sql,(_time,account_id,support_id,)) 
    data_all = cur.fetchall()
    cur.close() 
    conn.close() 
    a = len(data_all)
    # print('共有 '+ str(a) + ' 条记录')
    return data_all

def get_data(witness_or_committee, params):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": witness_or_committee,
            "params": params,
            "id":1
        }
        response = json.loads(requests.post(chain_api_url, data = json.dumps(body_relay), headers = headers).text)
        # print(response)
        witness_or_committee_result = response['result']
        #print('>> get_witness_or_committee\n {}\n'.format(witness_or_committee_result))
        return witness_or_committee_result
    except Exception as e:
        print(repr(e))


def get_total_votes():
    try:    
        account_real_ids = set()
        witnesses = get_data("lookup_witness_accounts", ["", 50])
        #print('>> get_witness_and_committee\n {}\n'.format(witness))
        witnesses_ids = []
        for witness in witnesses:
            witnesses_ids.append(witness[1])
        #print(witnesses_ids)
        witness_info = get_data("get_witnesses", [witnesses_ids])
        #print(witness_info)
        witnesses_total_votes = 0
        witnesses_vote_ids = []

        for witness in witness_info:
            witness['total_votes'] = int(witness['total_votes'])
        witness_info = sorted(witness_info, key=lambda x:x['total_votes'])
        witness_info.reverse()

        yestoday = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

        #print(len(witness_info))
        for witness in witness_info:
            witnesses_total_votes += witness['total_votes']
            witnesses_vote_ids.append(witness['vote_id'])
            
            witness_total_votes = format(round(witness['total_votes'] / 100000), ',')
            account_data = [datetime.datetime.now().strftime("%Y-%m-%d"), witness['id'],witness_total_votes, 0, witness['witness_account']]

            update_data("account", account_data)
            if not (witness['witness_account'] in account_names.keys()):
                account_real_ids.add(witness['witness_account'])

            supports = witness['supporters']
            for support in supports:
                support_amount = format(round(int(support[1]['amount']) / 100000), ',')
                support_amount_tmp = int(support[1]['amount'])
                supports_data = [datetime.datetime.now().strftime("%Y-%m-%d"), witness['id'], support[0], support_amount]
                update_data("supports", supports_data)
                if not (witness['witness_account'] in account_names.keys()):
                    account_real_ids.add(support[0])

                # account_supports_data = [datetime.datetime.now().strftime("%Y-%m-%d"), witness['id'], witness_total_votes, 0, support[0], support_amount]
                # update_data("account_supports", account_supports_data)

                support_yestody = select_data_with_ids("supports", yestoday, witness['id'], support[0])
                support_history = support_amount_tmp / 100000
                if support_history != None and len(support_yestody) != 0:
                    support_history = support_history - int(support_yestody[0][4].replace(',',''))
                support_history = format(round(support_history), ',')
                supports_analysis = [datetime.datetime.now().strftime("%Y-%m-%d"), witness['id'], support[0], 0, witness_total_votes,  support_amount, support_history, witness['witness_account']]
                update_data("supports_analysis", supports_analysis)

            if supports == '' or supports == None or len(supports) == 0:
                supports_analysis = [datetime.datetime.now().strftime("%Y-%m-%d"), witness['id'], "", 0, witness_total_votes,  "", "", witness['witness_account']]
                # print(supports_analysis)
                update_data("supports_analysis", supports_analysis)

            # 打印witness详细数据
            #print('>> witnesses:    {}, total_votes:    {}'.format(witness['witness_account'], witness['total_votes']))
        #包含重复print('\n>> witnesses_total_votes：  {}'.format(witnesses_total_votes))


        committeees = get_data("lookup_committee_member_accounts", ["", 50])
        #print('>> get_witness_and_committee\n {}\n'.format(committee))

        committeees_ids = []
        for committee in committeees:
            committeees_ids.append(committee[1])
        #print(witnesses_ids)
        committeees_info = get_data("get_committee_members", [committeees_ids])

        for committee in committeees_info:
            committee['total_votes'] = int(committee['total_votes'])
        committeees_info = sorted(committeees_info, key=lambda x:x['total_votes'])
        committeees_info.reverse()        
        
        committeees_total_votes = 0
        committeees_vote_ids = []
        for committee in committeees_info:
            committeees_total_votes += int(committee['total_votes'])
            committeees_vote_ids.append(committee['vote_id'])

            committee_total_votes = format(round(int(committee['total_votes']) / 100000), ',')
            account_data = [datetime.datetime.now().strftime("%Y-%m-%d"), committee['id'], committee_total_votes, 1, committee['committee_member_account']]
            #print(account_data)
            update_data("account", account_data)
            if not (witness['witness_account'] in account_names.keys()):
                account_real_ids.add(committee['committee_member_account'])

            supports = committee['supporters']
            for support in supports:
                support_amount_tmp = int(support[1]['amount'])
                support_amount = format(round(int(support[1]['amount']) / 100000 ), ',')
                supports_data = [datetime.datetime.now().strftime("%Y-%m-%d"), committee['id'], support[0], support_amount]
                update_data("supports", supports_data)
                if not (witness['witness_account'] in account_names.keys()):
                    account_real_ids.add(support[0])

                # account_supports_data = [datetime.datetime.now().strftime("%Y-%m-%d"), committee['id'], committee_total_votes, 1, support[0], support_amount]
                # update_data("account_supports", account_supports_data)


                support_yestody = select_data_with_ids("supports", yestoday, committee['id'], support[0])
                support_history = support_amount_tmp / 100000
                if support_yestody != None and len(support_yestody) != 0:
                    support_history = support_history - int(support_yestody[0][4].replace(',',''))
                support_history = format(round(support_history), ',')
                supports_analysis = [datetime.datetime.now().strftime("%Y-%m-%d"), committee['id'], support[0], 1, committee_total_votes,  support_amount, support_history, committee['committee_member_account']]
                update_data("supports_analysis", supports_analysis)

            if supports == '' or supports == None or len(supports) == 0:
                supports_analysis = [datetime.datetime.now().strftime("%Y-%m-%d"), committee['id'], "", 1, committee_total_votes,  "", "", committee['committee_member_account']]
                update_data("supports_analysis", supports_analysis)

            # 打印committee详细数据
            #print('>> committee:    {}, total_votes:    {}'.format(committee['committee_member_account'], committee['total_votes']))
        #包含重复print('>> committeees_total_votes： {}\n'.format(committeees_total_votes))
        #包含重复print('>> total_votes： {}\n'.format(committeees_total_votes + witnesses_total_votes))


        #-----witness去重-------
        witnesses_supporters = []
        witnesses_supporters_infos = get_data("lookup_vote_ids", [witnesses_vote_ids])
        for supporters in witnesses_supporters_infos:
            witnesses_supporters += supporters['supporters']

        witnesses_supporters_set = set()
        witnesses_supporters_total_votes = 0
        witnesses_double_counts = 0
        for supporter in witnesses_supporters:
            #print(supporter[1]['amount'])
            witnesses_supporters_total_votes += int(supporter[1]['amount'])
            tmp = supporter[0] + ':' +str(supporter[1]['amount'])   #1.2.32441:330000000
            if tmp in witnesses_supporters_set:
                witnesses_double_counts += int(supporter[1]['amount'])
            else:
                witnesses_supporters_set.add(tmp)


        witnesses_supporters_real_votes = format(round((witnesses_supporters_total_votes - witnesses_double_counts) / 100000), ',')
        witnesses_total_votes_s =  format(round((witnesses_total_votes - witnesses_double_counts) / 100000), ',')

        print('\n>> witnesses_supporters_real_votes： {}'.format(witnesses_supporters_real_votes))
        print('>> witnesses_total_votes：  {}'.format(witnesses_total_votes_s))

        #-----committee去重-------
        committeees_supporters = []
        committeees_supporters_infos = get_data("lookup_vote_ids", [committeees_vote_ids])
        for supporters in committeees_supporters_infos:
            committeees_supporters += supporters['supporters']

        #print(committeees_supporters)
        committeees_supporters_set = set()
        committeees_supporters_total_votes = 0
        committeees_double_counts = 0
        for supporter in committeees_supporters:
            #print(supporter[1]['amount'])
            committeees_supporters_total_votes += int(supporter[1]['amount'])
            tmp = supporter[0] + ':' +str(supporter[1]['amount'])
            if tmp in committeees_supporters_set:
                committeees_double_counts += int(supporter[1]['amount'])
            else:
                committeees_supporters_set.add(tmp)
                

        committeees_supporters_real_votes = format(round((committeees_supporters_total_votes - committeees_double_counts) / 100000), ',')
        committeees_total_votes_s = format(round((committeees_total_votes - committeees_double_counts) / 100000), ',')
        total_votes_s =  format(round((committeees_total_votes - committeees_double_counts + witnesses_total_votes - witnesses_double_counts) / 100000), ',')


        _data = [datetime.datetime.now().strftime("%Y-%m-%d"), total_votes_s, committeees_total_votes_s, committeees_supporters_real_votes, witnesses_total_votes_s, witnesses_supporters_real_votes]
        update_data("total_votes", _data)
        print('\n>> committeees_supporters_real_votes： {}'.format(committeees_supporters_real_votes))
        print('>> committeees_total_votes：  {}'.format(committeees_total_votes_s))
        print('\n>> total_votes： {}\n'.format(total_votes_s))

        account_names_data = get_data("get_accounts", [list(account_real_ids)])
        for name in account_names_data:
            name_data = [name['id'], name['name']]
            account_names[name['id']] = name['name']
            update_data("account_name", name_data)
        global IS_UPDATE_TODAY
        IS_UPDATE_TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
        wite_lock()
    except Exception as e:
        print(repr(e))

def updata_account_names(key):
    if key in account_names.keys():
        return
    account_data = get_data("get_accounts", [[key]])  
    for name in account_data:
        name_data = [name['id'], name['name']]
        account_names[name['id']] = name['name']
        update_data("account_name", name_data)  

def pack_accounts_data(now_time):
    if not account_names:
        account_names_data = select_all_data("account_name")
        for name in account_names_data:
            account_names[name['id']] = name['name']

    witness_data = select_data_with_time_type("account", now_time, 0)
    committee_data = select_data_with_time_type("account", now_time, 1)
    data = []
    witness_data = sorted(witness_data, key=lambda x:int(x[3].replace(',','')))
    committee_data = sorted(committee_data, key=lambda x:int(x[3].replace(',','')))
    i = len(witness_data)-1
    while i>=0:
        supports = []
        if len(witness_data[i]) > 0 :
            supports = select_data_with_time_type("supports", now_time, witness_data[i][2])
            j = 0
            while j <= len(supports)-1: 
                supports[j] = list(supports[j])
                if not (supports[j][3] in account_names.keys()):
                    updata_account_names(supports[j][3])
                supports[j][3] = account_names[supports[j][3]]  
                j += 1
        witness_data[i] = list(witness_data[i])
        if not (witness_data[i][5] in account_names.keys()):
            updata_account_names(witness_data[i][5])                
        witness_data[i][2] = account_names[witness_data[i][5]]
        tmp = [witness_data[i], supports]
        data.append(tmp)
        i-=1
    i = len(committee_data)-1
    while i>=0: 
        supports = []
        if len(committee_data[i]) > 0 :
            supports = select_data_with_time_type("supports", now_time, committee_data[i][2])
            j = 0
            while j <= len(supports)-1: 
                supports[j] = list(supports[j])
                if not (supports[j][3] in account_names.keys()):
                    updata_account_names(supports[j][3])     
                supports[j][3] = account_names[supports[j][3]]   
                j += 1
        committee_data[i] = list(committee_data[i])       
        if not (committee_data[i][5] in account_names.keys()):
            updata_account_names(committee_data[i][5])            
        committee_data[i][2] = account_names[committee_data[i][5]]                       
        tmp = [committee_data[i], supports]
        data.append(tmp)     
        i-=1
    return data      

def compare_id(account_id1, account_id2):
    if len(account_id1) == 0 and len(account_id2) == 0:
        return 0
    if len(account_id1) == 0 and len(account_id2) != 0:
        return -1
    if len(account_id1) != 0 and len(account_id2) == 0:
        return 1
    count_id1 = 0 if len(account_id1) == 0 else int(account_id1[len('1.2.'):])   
    count_id2 = 0 if len(account_id2) == 0 else int(account_id2[len('1.2.'):])   
    if count_id1 > count_id2:
        return 1
    elif count_id1 < count_id2:
        return -1
    else:
        return 0   

def packed_data(query_time):
    result = []    
    if len(query_time) == 0:
        return result

    if not account_names:
        account_names_data = select_all_data("account_name")
        for name in account_names_data:
            account_names[name['id']] = name['name']

    data = select_data_with_time("supports_analysis", query_time)
       
    data = sorted(data, key=lambda x:int(x[5].replace(',','')))   
    data.reverse()

    if data == '' or data == None or len(data) == 0:
        return result
    last_account = data[0]
    account_id = data[0][2]
    account_tmp = []
    result_tmp = []
    supports_tmp = []
    count = 1

    for account in data:        
        if account_id != account[2] and count != 1:
            account_tmp.append(last_account[0])
            account_tmp.append(last_account[1])
            # account_tmp.append(last_account[2])
            if not (last_account[8] in account_names.keys()):
                updata_account_names(last_account[8])              
            account_tmp.append(account_names[last_account[8]])
            account_tmp.append(last_account[5])
            account_tmp.append(last_account[4])            
            result_tmp.append(account_tmp)
            result_tmp.append(supports_tmp)
            result.append(result_tmp)              
            account_id = account[2]
            account_tmp = []
            result_tmp = []
            supports_tmp = [] 
            last_account = account
        support_tmp = []            
        support_tmp.append(count)
        support_tmp.append(account[1])
        support_tmp.append(account[2])
        # support_tmp.append(account[3])
        # support_tmp.append(account[3])
        if account[3] != '' and  account[3] != None:
            if not (account[3] in account_names.keys()):
                updata_account_names(account[3])              
            support_tmp.append(account_names[account[3]])
        else:
            support_tmp.append(account[3])
        support_tmp.append(account[6])        
        support_tmp.append(account[7]) 
        supports_tmp.append(support_tmp)       
        count += 1   
    account_tmp.append(last_account[0])
    account_tmp.append(last_account[1])
    # account_tmp.append(last_account[2])
    if not (last_account[8] in account_names.keys()):
        updata_account_names(last_account[8])              
    account_tmp.append(account_names[last_account[8]])      
    account_tmp.append(last_account[5])
    account_tmp.append(last_account[4])                     
    result_tmp.append(account_tmp)
    result_tmp.append(supports_tmp)
    result.append(result_tmp)                
    return result

def pack_accounts_compare_data(start_time, end_time):
    data = []   
    s_time = time.mktime(time.strptime(start_time,'%Y-%m-%d'))
    e_time = time.mktime(time.strptime(end_time,'%Y-%m-%d'))
    one_day = (int(e_time) - int(s_time))/60/60/24

    if one_day == 1:
        query_time = end_time
        data = packed_data(query_time)    
        return data

    else:
        print("todo...")
        # accounts_data_start = select_data_with_time("supports_analysis", start_time)
        # accounts_data = set(accounts_data_start)
        # accounts_data_end = select_data_with_time("supports_analysis", end_time)
        # accounts_data.update(accounts_data_end)
        # for account in accounts_data:
        #     supports_start = select_data_with_time_type("supports", start_time, account[2])
        #     supports_end = select_data_with_time_type("supports", end_time, account[2])

        #     supports = []
        #     supports_length = len(supports_start) if len(supports_start) >= len(supports_end) else len(supports_end)   
        #     i = supports_length - 1
        #     j = supports_length - 1
        #     while i >= 0 or j >= 0:


        #     tmp = [account, supports_end, ]
        #     data.append(tmp)

    return data      

# 每DAY执行一次
def get_lock_cocos_amount_loop():
    init_tables()
    while True:
        print(datetime.datetime.now().strftime("%Y-%m-%d"))
        global IS_UPDATE_TODAY
        if(IS_UPDATE_TODAY != datetime.datetime.now().strftime("%Y-%m-%d")):
            get_total_votes()
        if QUIT:
            sys.exit(0)
        time.sleep(DAY)

class DeriveThread(threading.Thread):
    def __init__(self, name, do_action):
        threading.Thread.__init__(self)
        self.name = name
        self.do_action = do_action

    def run(self):
        memo = str(self.name) + ' '
        print('[run] {m} run start '.format(m = memo))
        try:
            self.do_action()
        except Exception as e:
            print(repr(e))


class DemoHttpServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # if self.path == '/witness':
        #     # data = select_data_with_time("account", datetime.datetime.now().strftime("%Y-%m-%d"), 0)
        #     print(datetime.datetime.now().strftime("%Y-%m-%d"))
        #     data = select_data_with_time("account", "2020-05-20", 0)
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return      

        # elif self.path == '/committee':
        #     data = select_data_with_time("account", datetime.datetime.now().strftime("%Y-%m-%d"), 1)
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return     

        # elif self.path == '/supports/witness':
        #     data = select_data_with_time("account_supports", datetime.datetime.now().strftime("%Y-%m-%d"), 0)
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return        

        # elif self.path == '/supports/committee':
        #     data = select_data_with_time("account_supports", datetime.datetime.now().strftime("%Y-%m-%d"), 1)
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/html')
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return      

        # elif self.path.find('/accounts') != -1:
        #     now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        #     if self.path != '/accounts':
        #         now_time = self.path[len('/accounts')+1:]
        #     data = pack_accounts_data(now_time)
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/json')
        #     self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        #     self.send_header("Pragma", "no-cache")
        #     self.send_header("Expires", "0")
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return

        # elif self.path.find('/supports/account') != -1:
        #     account_id = self.path[len('/supports/account')+1:]
        #     data = select_data_with_time("supports", datetime.datetime.now().strftime("%Y-%m-%d"), account_id)
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return      

        # elif self.path == '/test.json':
        #     data = [{"333":"44","version":"1.2.1","fruit":[{"apple":"one"},{"banana":"two"},{"grap":"three"},{"orange":"four"}]},\
        #      {"333":"44","version":"1.2.3","fruit":[{"apple":"one"},{"banana":"two"},{"grap":"three"},{"orange":"four"}]}]
        #     resp = json.dumps(data,indent=4)
        #     self.send_response(200, message='OK')
        #     self.send_header('Content-Type', 'application/json')
        #     self.end_headers()
        #     self.wfile.write(resp.encode())
        #     return

        if self.path == '/home':
            path = os.getcwd()
            resp = ""
            try:
                _path = path + FILE_NAME
                print(_path)
                file = open(_path, "rb")
                resp = file.read()
                file.close()
            except IOError:
                resp = "The file is not found!".encode()
                    
            self.send_response(200, message='OK')
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")            
            self.end_headers()
            self.wfile.write(resp)
            return

        elif self.path.find('/accounts') != -1:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d")
            if self.path != '/accounts':
                now_time = self.path[len('/accounts')+1:]
            data = pack_accounts_data(now_time)
            resp = json.dumps(data,indent=4)
            self.send_response(200, message='OK')
            self.send_header('Content-Type', 'application/json')
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()
            self.wfile.write(resp.encode())
            return

        elif self.path.find('/compare_accounts') != -1:
            start_end_time = self.path[len('/compare_accounts')+1:]
            start_time = start_end_time[len('start_time='):start_end_time.find('/end_time=')]
            end_time = start_end_time[start_end_time.find('/end_time=')+len('/end_time='):]
            data = pack_accounts_compare_data(start_time, end_time)

            resp = json.dumps(data,indent=4)
            self.send_response(200, message='OK')
            self.send_header('Content-Type', 'application/json')
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")            
            self.end_headers()
            self.wfile.write(resp.encode())
            return

        elif self.path.find('/supports/account') != -1:
            query_time = self.path[len('/supports/account')+1:]
            yestoday = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            data = select_data_with_time("supports", query_time)
            resp = json.dumps(data,indent=4)
            self.send_response(200, message='OK')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.encode())
            return  

        elif self.path == '/delete':
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            print(today)
            delete_datas("account", today)
            delete_datas("supports", today)
            delete_datas("supports_analysis", today)
            resp = "Today data clear..."
            self.send_response(200, message='OK')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.encode())
            return  

        elif self.path.find('/quit') != -1:
            account = self.path[len('/quit')+1:]
            resp = "system is exit..."
            if hashlib.md5(account.encode()).hexdigest() != "7b698222ddcc6c5fac801f93e570c982":
                resp = "error account..."
            self.send_response(200, message='OK')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.encode())    
            if hashlib.md5(account.encode()).hexdigest() != "7b698222ddcc6c5fac801f93e570c982":
                return            
            global QUIT 
            QUIT = 1
            sys.exit(0)
            return

        else :
            self.send_error(404, "Page not Found!")
            return



def start_server():
    server = HTTPServer(('0.0.0.0', 8008), DemoHttpServer)
    print('Server is running...')
    server.serve_forever()


def app():
    threads = []
    name = 'thread-' + 'get_lock_cocos_amount_loop'
    thread = DeriveThread(name, get_lock_cocos_amount_loop)        #---------------------------------
    thread.start()
    threads.append(thread)

    server = 'thread-' + 'start_server'
    server_thread = DeriveThread(server, start_server)        #---------------------------------
    server_thread.start()
    threads.append(server_thread)

    # 等待所有线程完成
    for t in threads:
        t.join()


# test...
# account_ids = []
# account_ids.append('1.2.28598')
# account_ids.append('1.2.35842')
# test = get_data("get_accounts", [account_ids])
# print(test)

# account_ids = []
# account_ids.append('1.5.19')
# account_ids.append('1.5.20')
# test = get_data("get_committee_members", [account_ids])
# print(test)


if __name__ == '__main__':
    app()



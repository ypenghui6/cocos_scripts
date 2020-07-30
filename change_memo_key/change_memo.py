# -*- coding:utf-8 -*-

import json
import requests
import os
import configparser  


headers = {"content-type": "application/json"}
cli_wallet_url = "http://0.0.0.0:8099"
newfile = "change_memo88.txt"
account = "vote2test"
memo_key = None


def save_account(str):
    global newfile    
    if not os.path.exists(newfile):
        f = open(newfile,'w')
        f.write(str+'\n')
        f.close()
    else:
        f = open(newfile,'a')
        f.write(str+'\n')
        f.close()
    return


def read_config():
    print("read config...")
    if not os.path.exists("config.cfg"):
        print("The configuration file does not exist,use default configuration.")
        return
    conf = configparser.RawConfigParser()  
    conf.read("config.cfg")  

    if not conf.has_section('config'):
        print("The configuration file has an error.")
        return

    global account
    global newfile
    global cli_wallet_url
    global memo_key

    if conf.has_option('config', 'account'):
        account = conf.get("config", "account")

    if conf.has_option('config', 'newfile'):
        newfile = conf.get("config", "newfile")

    if conf.has_option('config', 'cli_wallet_url'):
        cli_wallet_url = conf.get("config", "cli_wallet_url")

    if conf.has_option('config', 'memo_key'):
        memo_key = conf.get("config", "memo_key")


def is_locked():
    try:
        global cli_wallet_url
        body_relay = {
            "jsonrpc": "2.0",
            "method": "is_locked",
            "params": [],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> is_locked\n {}\n'.format(result)
        return result
    except Exception as e:
        print(repr(e))
        return 1

def suggest_brain_key():
    try:
        global cli_wallet_url     
        body_relay = {
            "jsonrpc": "2.0",
            "method": "suggest_brain_key",
            "params": [],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> suggest_brain_key\n {}\n'.format(result)
        save_account(result_str)
        return result
    except Exception as e:
        print(repr(e))
        return None

def get_account(_account_name):
    try:
        global cli_wallet_url      
        body_relay = {
            "jsonrpc": "2.0",
            "method": "get_account",
            "params": [_account_name],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> get_account\n {}\n'.format(result)
        save_account(result_str)
        return result
    except Exception as e:
        print(repr(e))
        return None

def pack_parameters(_account_name):
    try:
        print("get account...")
        global cli_wallet_url
        global memo_key        
        if memo_key == None or len(memo_key) != 55:
            result = suggest_brain_key()
            if not result:
                return
            memo_key = result['pub_key']
            memo_key_str = '>> memo_key: {}\n'.format(memo_key)
            save_account(memo_key_str)

        _account = get_account(_account_name)
        if not _account:
            return
        _account_id = _account['id']
        _account_votes = _account['options']['votes']
        _account_extensions = _account['options']['extensions']

        result = {"account":_account_id,"new_options":{"memo_key":memo_key,"votes":_account_votes,"extensions":_account_extensions}}
        return result
    except Exception as e:
        print(repr(e))
        return None

def begin_builder_transaction():
    try:
        global cli_wallet_url        
        print("begin builder transaction...")        
        body_relay = {
            "jsonrpc": "2.0",
            "method": "begin_builder_transaction",
            "params": [],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> begin_builder_transaction\n {}\n'.format(result)
        save_account(result_str)
        return result
    except Exception as e:
        print(repr(e))
        return None

def add_operation_to_builder_transaction(_b_result, op_update):
    try:
        global cli_wallet_url       
        print("add operation to builder transaction...")            
        body_relay = {
            "jsonrpc": "2.0",
            "method": "add_operation_to_builder_transaction",
            "params": [_b_result,[6, op_update]],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> add_operation_to_builder_transaction\n {}\n'.format(result)
        save_account(result_str)
        return result_str
    except Exception as e:
        print(repr(e))
        return None

def sign_builder_transaction(_b_result):
    try:
        global cli_wallet_url      
        print("sign builder transaction...")             
        body_relay = {
            "jsonrpc": "2.0",
            "method": "sign_builder_transaction",
            "params": [_b_result, 1],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> sign_builder_transaction\n {}\n'.format(result)
        save_account(result_str)
        return result_str
    except Exception as e:
        print(repr(e))
        return None

def change_memo():
    if is_locked():
        print("Please unlock cli_wallet fisrt...\n")
        return
    global account   
    global memo_key   

    read_config()

    save_account("change memo begin......\n")

    op_update = pack_parameters(account)

    b_result = begin_builder_transaction()
    if b_result == None:
        print('change memo failed...\n')
        return
    a_result = add_operation_to_builder_transaction(b_result, op_update)
    if a_result == None:
        print('change memo failed...\n')
        return
    s_result = sign_builder_transaction(b_result)
    if s_result == None:
        print('change memo failed...\n')
        return
    print('memo key：{}\n'.format(memo_key))
    print('You can view the private key in the file, If the key is generated by the system.\n')
    print('change memo success...\n')
    save_account("change memo success......\n")

change_memo()       


''' 
example: 
python3 change_memo.py

read config...
get account...
begin builder transaction...
add operation to builder transaction...
sign builder transaction...
memo key：COCOS72QWc65vb7jdwZGbiwtvX69Xh9sb76oP3gRovmRFz9M2wGmN99

You can view the private key in the file, If the key is generated by the system.

change memo success...


#config不配置memo key，系统自动生成memo key
python3 change_memo.py

read config...
get account...
begin builder transaction...
add operation to builder transaction...
sign builder transaction...
memo key：COCOS5G7uWRGbxq6iy9xF5DdbtKQomCkvyJuTe8iLNk5Pj29hxssMTp

You can view the private key in the file, If the key is generated by the system.

change memo success...

'''


# -*- coding:utf-8 -*-

import json
import requests
import os

#cli_wallet_url = "http://0.0.0.0:8048"
cli_wallet_url = "http://0.0.0.0:8099"
headers = {"content-type": "application/json"}
register_account_name = 'nicotest'
newfile = "accounts.txt"
accounts = [
'cocos67-root',
'cocos67-init0',
'cocos67-init0',
'cocos67-init0',
'cocos67-init3',
'cocos67-init4'
]

def get_account(name):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": "get_account",
            "params": [name],
            "id":1
        }
        account_info = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        account_object = account_info['result']
        print('>> get the account: {}\n'.format(account_object))
        return account_object
    except Exception as e:
        print(repr(e))
        return None

def suggest_brain_key():
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": "suggest_brain_key",
            "params": [],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        brain_key = response['result']
        print('>> suggest_brain_key\n {}\n'.format(brain_key))
        return brain_key
    except Exception as e:
        print(repr(e))

#register = "nicotest"
def register_account(register, new_account_name):
    account_object = get_account(new_account_name)
    if account_object != None:
        print('>> occur error:  you hava regiter the account: {}\n'.format(new_account_name))
        return
    owner_brain_key = suggest_brain_key()
    active_brain_key = suggest_brain_key()
    owner_pub_key = owner_brain_key['pub_key']   
    active_pub_key = active_brain_key['pub_key']
    print('>> register_account {} {} {} {} {}\n'.format(new_account_name, owner_pub_key, active_pub_key, register, 'true'))
    try:    
        body_relay = {
            "jsonrpc": "2.0",
            "method": "register_account",
            "params": [new_account_name, owner_pub_key, active_pub_key, register, 1],
            "id":1
        }
        json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        account_object = get_account(new_account_name)

        if account_object == None:
            print('>> occur error:  failed to regiter the account: {}\n'.format(new_account_name))
            return
        save_result = {"name":new_account_name, "owner_pub_key":owner_pub_key, "owner_priv_key":owner_brain_key['wif_priv_key'],"active_pub_key":active_pub_key, "active_priv_key":active_brain_key['wif_priv_key']} 
        tmp = json.dumps(save_result)
        save_account(tmp)
        print('>> get_account {} \n{}\n'.format(new_account_name, account_object))
    except Exception as e:
        print(repr(e))

#test

def register_accounts():
    for _account in accounts:
        register_account(register_account_name, _account)


def save_account(str):
    if not os.path.exists(newfile):
        f = open(newfile,'w')
        print(newfile)
        f.write(str+'\n')
        f.close()
    else:
        f = open(newfile,'a')
        f.write(str+'\n')
        f.close()
    return


register_accounts()       

''' 
example: 
python create_account.py 

>> suggest_brain_key
 {'wif_priv_key': '5K2t8Y9P9KzMxJ9D6CK5h7HFzspb2zJyMvAVAcwPzaLahjEbcYd', 'brain_priv_key': 'QUARTAN AAM CUPRITE ROPY BUCKY FITTY TERMA PLOTE CATTAIL BERRET JINNY LADYISH TOW GOMUTI WITTING GARVOCK', 'address_info': 'COCOS4JmiPSsTxSjo6QfVZfSrPNf2AKvLdyiVo', 'pub_key': 'COCOS8WwAQmcjXBqNt2gwpQERzT6GVjqQHq8RCzMhNNPjK1BWQ99dE4'}

>> suggest_brain_key
 {'wif_priv_key': '5JGmmgByTJNzxAfAVDECT7Q2SQ7omro8eGxZSMyRcxwMhWqpTvr', 'brain_priv_key': 'AMINE BASALLY SAFENER CASSINO CANTRED TURBITH CHOIR SCHOLIA SEA CYMBA WOULDNT SERRANO BESCOUR INSHELL BEGLUC GAGROOT', 'address_info': 'COCOS2Tg23NPNsgHYhjQd9niCUZEEFa645Bea4', 'pub_key': 'COCOS64vuKNKijR8utnz6MH83A58YXCsy4gA9XtBTe1uabKadBZFGCz'}

>> register_account test81 COCOS8WwAQmcjXBqNt2gwpQERzT6GVjqQHq8RCzMhNNPjK1BWQ99dE4 COCOS64vuKNKijR8utnz6MH83A58YXCsy4gA9XtBTe1uabKadBZFGCz nicotest true

>> get_account test81 
{'options': {'memo_key': 'COCOS64vuKNKijR8utnz6MH83A58YXCsy4gA9XtBTe1uabKadBZFGCz', 'votes': [], 'extensions': []}, 'membership_expiration_date': '1970-01-01T00:00:00', 'asset_locked': {'contract_lock_details': [], 'locked_total': []}, 'owner': {'weight_threshold': 1, 'account_auths': [], 'key_auths': [['COCOS8WwAQmcjXBqNt2gwpQERzT6GVjqQHq8RCzMhNNPjK1BWQ99dE4', 1]], 'address_auths': []}, 'active': {'weight_threshold': 1, 'account_auths': [], 'key_auths': [['COCOS64vuKNKijR8utnz6MH83A58YXCsy4gA9XtBTe1uabKadBZFGCz', 1]], 'address_auths': []}, 'id': '1.2.269', 'registrar': '1.2.16', 'statistics': '2.6.269', 'name': 'test81'}

'''


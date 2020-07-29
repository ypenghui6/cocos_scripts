# -*- coding:utf-8 -*-

import json
import requests
import os

#cli_wallet_url = "http://0.0.0.0:8048"
cli_wallet_url = "http://0.0.0.0:8099"
headers = {"content-type": "application/json"}
newfile = "nh_asset.txt"

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


def create_nh_asset():
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": "create_nh_asset",
            "params": ["fee2test","fee2test","1.3.0","ypp","test nh asset create 2", 1],
            "id":1
        }
        response = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        result = response['result']
        result_str = '>> create_nh_asset\n {}\n'.format(result)
        print(result_str)
        save_account(result_str)
        return result
    except Exception as e:
        print(repr(e))

def create_nh_assets(_counts):
    num = _counts
    while num > 0:
        create_nh_asset()
        num -= 1

create_nh_assets(10000)       

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


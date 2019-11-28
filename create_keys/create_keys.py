# -*- coding:utf-8 -*-

import json
import requests
import os

cli_wallet_url = "http://0.0.0.0:8066"
headers = {"content-type": "application/json"}
newfile = "bps.txt"
keys_counts = 12

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


def create_keys():
    count = 0
    while count < keys_counts:
        count = count + 1
        account_key = suggest_brain_key()
        tmp = json.dumps(account_key)
        save_account(tmp)
            

create_keys()

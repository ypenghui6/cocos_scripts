# -*- coding:utf-8 -*-

import json
import requests
import os

cli_wallet_url = "http://0.0.0.0:8066"
headers = {"content-type": "application/json"}
bps_keys_file = "bps_keys.txt"
bps_pub_keys_file = "bps_pub_keys.txt"
bps_wif_priv_keys_file = "bps_wif_priv_keys.txt"
bps_brain_priv_keys_file = "bps_brain_priv_keys.txt"

keys_counts = 13

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


def save_account(str, newfile):
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

        tmp_key = json.dumps(account_key)
        save_account(tmp_key, bps_keys_file)

        tmp_pub_key = json.dumps(account_key['pub_key'])
        save_account(tmp_pub_key, bps_pub_keys_file)

        tmp_priv_key = json.dumps({"wif_priv_key":account_key['wif_priv_key'], "pub_key":account_key['pub_key']})
        save_account(tmp_priv_key, bps_wif_priv_keys_file)

        tmp_brain_priv_key = json.dumps({"brain_priv_key":account_key['brain_priv_key'], "pub_key":account_key['pub_key']})
        save_account(tmp_brain_priv_key, bps_brain_priv_keys_file)            


create_keys()

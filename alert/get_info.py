# -*- coding:utf-8 -*-

import json
import requests
import os
from websocket import create_connection
#cli_wallet_url = "http://api.cocosbcx.net"
headers = {"content-type": "application/json"}
#chain_api_url = "https://test.cocosbcx.net"  
chain_api_url = "https://api.cocosbcx.net"
chengdu_api_url = "ws://47.244.211.84:8701"  

    
def get_data(chain_head_num, params, _chain_api_url):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": chain_head_num,
            "params": params,
            "id":1
        }
        response = json.loads(requests.post(_chain_api_url, data = json.dumps(body_relay), headers = headers).text)
        #print(response)
        witness_or_committee_result = response['result']
        #print('>> get_witness_or_committee\n {}\n'.format(witness_or_committee_result))
        print(witness_or_committee_result['head_block_number'])
        return witness_or_committee_result['head_block_number']
    except Exception as e:
        print(repr(e))

def get_ws_data(chain_head_num, _chain_api_url):
    try:
        ws = create_connection(_chain_api_url)

        print("Sending 'Hello, World'...")
        data1={"id":0,"method":"call","params":[0,chain_head_num,[]]}

        ws.send(json.dumps(data1))
        print("Sent")
        print("Receiving...")
        result1 =  ws.recv()
        ws.close()

        result1 =  json.loads(result1)
        result = result1["result"]
        result = result['head_block_number']
        print(result)
        return result
    except Exception as e:
        print(repr(e))       

def warn(peer_error_num, peer_good_num):
    try:
        if (peer_error_num - peer_error_num > 2000 | peer_error_num - peer_error_num < -2000):
            print("warn: please check the peer !!!")
    except Exception as e:
        print(repr(e))



peer_error_num = get_data("get_dynamic_global_properties",[], chain_api_url)
peer_good_num = get_ws_data("get_dynamic_global_properties", chengdu_api_url)
#warn(peer_error_num, peer_good_num)


#testurl = "ws://47.111.249.169:8049"
#print(get_ws_data("get_dynamic_global_properties", testurl))

#testurl = "ws://121.89.217.90:8049"
#print(get_ws_data("get_dynamic_global_properties", testurl))

#testurl = "ws://121.89.217.90:8049"
#print(get_ws_data("get_dynamic_global_properties", testurl))

testurl = "https://10.22.0.14:8049"
#print(get_ws_data("get_dynamic_global_properties", testurl))
print(get_data("get_dynamic_global_properties",[], testurl))
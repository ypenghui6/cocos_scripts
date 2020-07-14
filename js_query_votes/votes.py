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
    infos = get_data("lookup_vote_ids", [["1:0"]])
    print(infos)


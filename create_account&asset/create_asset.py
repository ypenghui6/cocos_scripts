# -*- coding:utf-8 -*-

import json
import requests
import os

#cli_wallet_url = "http://0.0.0.0:8048"
cli_wallet_url = "http://0.0.0.0:8047"
headers = {"content-type": "application/json"}
creater_asset_name = 'nicotest'
newfile = "assets_history.txt"

market_assets = [
 'BTC',
 'XRP',
 'ETH',
 'BCH',
 'BCC', 
 'USD',
 'USDT',
 'LTC',
 'EOS',
 'BNB',
 'BSV',
 'XLM',
 'TRX',
 'NEO',
 'OIL',
 'SILVER',
 'GOLD',
 'COIN',
 'TRY',
 'SGD',
 'HKD',
 'RUB',
 'SEK',
 'NZD',
 'CNY',
 'MXN',
 'CAD',
 'CHF',
 'AUD',
 'GBP',
 'JPY',
 'EUR'
]

user_assets = [
]

user_asset_common = {"max_supply":"2100000000000000","market_fee_percent":0,"max_market_fee":0,"flags":0,"core_exchange_rate":{"base":{"amount":1,"asset_id":"1.3.4"},"quote":{"amount":1,"asset_id":"1.3.0"}},"description":"","extensions":[]} 
market_asset_common = {"issuer_permissions": 511,"flags": 0,"core_exchange_rate":{"base":{"amount":1,"asset_id":"1.3.3"},"quote":{"amount":1,"asset_id":"1.3.0"}}} 
bitasset_opts = {"new_feed_producers":[],"feed_lifetime_sec":120} 



def get_asset(_asset):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": "get_asset",
            "params": [_asset],
            "id":1
        }
        asset_info = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        print(asset_info)
        print("\n")
        save_account(json.dumps(asset_info))
        return asset_info
    except Exception as e:
        print(repr(e))


def create_user_asset(_asset):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": "create_asset",
            "params": [creater_asset_name, _asset, 8, user_asset_common, None, "true"],
            "id":1
        }
        create_user_asset_info = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        print(create_user_asset_info)
        print("\n")
        save_account(json.dumps(create_user_asset_info))
        return create_user_asset_info
    except Exception as e:
        print(repr(e))




def create_market_asset(_asset):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": "create_asset",
            "params": [creater_asset_name, _asset, 8, market_asset_common, bitasset_opts, "true"],
            "id":1
        }
        create_market_asset_info = json.loads(requests.post(cli_wallet_url, data = json.dumps(body_relay), headers = headers).text)
        print(create_market_asset_info)
        print("\n")
        save_account(json.dumps(create_market_asset_info))
        return create_market_asset_info
    except Exception as e:
        print(repr(e))



def create_assets():  
    
    for _asset in market_assets:
        create_market_asset(_asset)
        get_asset(_asset)
        
    for _asset in user_assets:
        create_user_asset(_asset)
        get_asset(_asset)
      

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



create_assets()       

'''
example: 
python create_account.py 
{'id': 1, 'result': ['88d7032f1c83feac5cbbf386af17f7251a091ffefcbf599e9a4fd695b03b6c6d', {'extensions': [], 'ref_block_prefix': 2514403900, 'signatures': ['1f25814751037219d7f41d32e905dd55c8beef88d12bacb1285a6769e9313d8cb90c4d50ea6641f9f7fab23a1ca87d05a666b07174c8442f2590b87b53626b209e'], 'expiration': '2019-11-21T06:18:54', 'operations': [[8, {'issuer': '1.2.16', 'precision': 8, 'common_options': {'issuer_permissions': 15, 'description': '', 'extensions': [], 'max_supply': '2100000000000000', 'market_fee_percent': 0, 'core_exchange_rate': {'base': {'amount': 1, 'asset_id': '1.3.4'}, 'quote': {'amount': 1, 'asset_id': '1.3.0'}}, 'max_market_fee': 0, 'flags': 0}, 'symbol': 'PNSUC', 'extensions': []}]], 'ref_block_num': 5261}], 'jsonrpc': '2.0'}

{'id': 1, 'result': {'id': '1.3.22', 'symbol': 'PNSUC', 'dynamic_asset_data_id': '2.3.22', 'issuer': '1.2.16', 'options': {'issuer_permissions': 15, 'description': '', 'extensions': [], 'max_supply': '2100000000000000', 'market_fee_percent': 0, 'core_exchange_rate': {'base': {'amount': 1, 'asset_id': '1.3.22'}, 'quote': {'amount': 1, 'asset_id': '1.3.0'}}, 'max_market_fee': 0, 'flags': 0}, 'precision': 8}, 'jsonrpc': '2.0'}




'''

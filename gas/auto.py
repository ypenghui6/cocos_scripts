import json
import requests

cli_wallet_url = "http://127.0.0.1:8048"

headers = {"content-type": "application/json"}
#test_faucet1_account = 'faucet1'
#test_faucet1_account_public_key = 'COCOS4z37sP33MsZS3a94RW3gukpunTcod5yZNDvJskPuhUtDf8Q9rp'
#test_faucet1_account_private_key = '5JcR8oHjMAFqKVdx3SSwM1FfwrbMHrGJqggu8Y594JhRjkgbz3b'

test_faucet1_account = 'cocos-test01'
test_faucet1_account_public_key = 'COCOS5Txw57dtwi5hRvafbTjPUtXiPmwmrNovmHYxLku4VAz5kNTUBL'
test_faucet1_account_private_key = '5KiAXE4GnfohNrcJNPeeVzyyZQyAYwVsSSqpGkctdYCZR5317g9'

test_faucet1_account_id = '1.2.40'
test_faucet1_account_vesting_id = '1.13.13'

#查询
req_data = {

    "jsonrpc": "2.0",

    "method": "get_vesting_balances",

    "params": [test_faucet1_account],

    "id":1

    }

response = json.loads(requests.post(cli_wallet_url, data = json.dumps(req_data), headers = headers).text)
print('>> {} {}\n{}\n'.format(req_data['method'], req_data['params'], response))


#申领
for withdraw in response['result']:

    print('withdraw: {}'.format(withdraw))

    withdraw = withdraw['allowed_withdraw']
    
    amount  = withdraw['amount']/100000

    a = ("%.5f" % amount)
    asset_id = withdraw['asset_id']

    req_data1 = {

        "jsonrpc": "2.0",

        "method": "withdraw_vesting",

        "params": [test_faucet1_account_vesting_id, a, asset_id, 'true'],

        "id":1

    }

response1 = json.loads(requests.post(cli_wallet_url, data = json.dumps(req_data1), headers = headers).text)

print( req_data1)
print('>> {} {}\n{}\n'.format(req_data['method'], req_data['params'], response1))

#再抵押

for withdraw in response['result']:

    print('withdraw: {}'.format(withdraw))

    withdraw = withdraw['allowed_withdraw']

    amount  = withdraw['amount']
    
    print(amount)

    asset_id = withdraw['asset_id']

    req_data2 = {

        "jsonrpc": "2.0",

        "method":"update_collateral_for_gas",

        "params": [test_faucet1_account_id,test_faucet1_account_id,amount,'true'],

        "id":1

    }

response2 = json.loads(requests.post(cli_wallet_url, data = json.dumps(req_data2), headers = headers).text)

print(req_data2)
print('>> {} {}\n{}\n'.format(req_data2['method'], req_data2['params'], response2))
	




# -*- coding:utf-8 -*-

import json
import requests
import os

#cli_wallet_url = "http://api.cocosbcx.net"
headers = {"content-type": "application/json"}
#chain_api_url = "https://test.cocosbcx.net"  
chain_api_url = "https://api.cocosbcx.net"  

    
def get_data(witness_or_committee, params):
    try:
        body_relay = {
            "jsonrpc": "2.0",
            "method": witness_or_committee,
            "params": params,
            "id":1
        }
        response = json.loads(requests.post(chain_api_url, data = json.dumps(body_relay), headers = headers).text)
        #print(response)
        witness_or_committee_result = response['result']
        #print('>> get_witness_or_committee\n {}\n'.format(witness_or_committee_result))
        return witness_or_committee_result
    except Exception as e:
        print(repr(e))


def get_total_votes():
    try:    
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
            witnesses_total_votes += int(witness['total_votes'])
            witnesses_vote_ids.append(witness['vote_id'])
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
        #print(witness_info)
        committeees_total_votes = 0
        committeees_vote_ids = []
        for committee in committeees_info:
            committeees_total_votes += int(committee['total_votes'])
            committeees_vote_ids.append(committee['vote_id'])
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


        print('\n>> committeees_supporters_real_votes： {}'.format(committeees_supporters_real_votes))
        print('>> committeees_total_votes：  {}'.format(committeees_total_votes_s))
        print('\n>> total_votes： {}\n'.format(total_votes_s))
    except Exception as e:
        print(repr(e))

get_total_votes()


''' 
example: 
python3 .\get_lock_cocos_amount.py


>> witnesses_supporters_real_votes： 282,395,699
>> witnesses_total_votes：  1,482,395,699

>> committeees_supporters_real_votes： 4,105
>> committeees_total_votes：  700,004,105

>> total_votes： 2,182,399,804

'''


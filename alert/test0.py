from websocket import create_connection
import datetime
import json
import redis
import requests
import time
import signal

def send_msg(subject, message):
    tokenid = "33e90c73e8e4f7ef4640bdf547ae7ca1a2e9e0ecd2075c1d75b2c2e69bca4d35"
#    tokenid = "3dea10d1d4370b1edc9c26c7b2812318ee5bf06c8b243a26352a10c8234ed2b0"
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + tokenid
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": subject + '\n' + message
        },
        "at": {
            "atMobiles": [
                "13552589586"

            ],
            "isAtAll": False
        }
    }
    sendData = json.dumps(data)
    # request = urllib2.Request(url, data=sendData, headers=header)
    urlopen = requests.post(url=url,headers=header,data=sendData)
    return urlopen.text

def set_timeout(num, callback):
  def wrap(func):
    def handle(signum, frame): # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
      raise RuntimeError
  
    def to_do(*args, **kwargs):
      try:
        signal.signal(signal.SIGALRM, handle) # 设置信号和回调函数
        signal.alarm(num) # 设置 num 秒的闹钟
        print 'start alarm signal.'
        r = func(*args, **kwargs)
        print 'close alarm signal.'
        signal.alarm(0) # 关闭闹钟
        return r
      except RuntimeError as e:
        callback()
  
    return to_do
  
  return wrap

def after_timeout(): # 超时后的处理函数
    print "timeout, pass..."
    return 0  

@set_timeout(2, after_timeout) # 限时 2 秒
def get_ws_data(chain_head_num, _chain_api_url):
    try:
        ws = create_connection(_chain_api_url)

        data1={"id":0,"method":"call","params":[0,chain_head_num,[]]}

        ws.send(json.dumps(data1))
        print("Sent")
        print("Receiving...")
        result1 =  ws.recv()
        ws.close()

        result1 =  json.loads(result1)
        result = result1["result"]
        result = result['head_block_number']
        return result
    except Exception as e:
        print(repr(e))     
        return 0  



ws1 = create_connection("wss://api.cocosbcx.net")

print("Sending 'Hello, World'...")
data1={"id":4,"method":"call","params":[1,"network_node",[]]}

ws1.send(json.dumps(data1))
print("Sent")
print("Receiving...")
result1 =  ws1.recv()
result1 =  json.loads(result1)
app_id1 = result1["result"]
data1={"id":0,"method":"call","params":[app_id1,"get_connected_peers",[]]}
ws1.send(json.dumps(data1))
result1 =  ws1.recv()
result1 =  json.loads(result1)
data1 = result1["result"]
ip_list=[]
for block in data1:
    ip = block["host"]
    num = block["info"]["current_head_block_number"]
    print(ip,num)
    ip_list.append({"ip":ip,"num":num})
ws1.close()
ws = create_connection("ws://10.22.0.2:8049")

print("Sending 'Hello, World'...")
data={"id":4,"method":"call","params":[1,"network_node",[]]}

ws.send(json.dumps(data))
print("Sent")
print("Receiving...")
result =  ws.recv()
result = json.loads(result)
print("-----------------------------------")
app_id = result["result"]
data2={"id":0,"method":"call","params":[app_id,"get_connected_peers",[]]}
ws.send(json.dumps(data2))
result =  ws.recv()
result =  json.loads(result)
data = result["result"]
print("=================================")
print(result)
print("=====================================================================")
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
registry = CollectorRegistry()
r = redis.StrictRedis(host="localhost",port=6379,db=0)
region_list=["beijing-bp: 120.77.226.49","成都: 47.244.211.84","闪电： 47.106.22.215","hashquark: 152.32.170.134","浩方: 47.52.188.115","yisucapital: 47.113.82.90","君物: 39.104.77.231","超开心: 47.111.249.169","alvin个人: 39.101.134.20"]
list_nums=[]
g = Gauge('node', '连接节点数',['dst_ip','env'], registry=registry)
for info in data:
    ip = info["host"]
    num = info["info"]["current_head_block_number"]
    print("-------%s----------------"%ip)
    if ip == "10.22.0.2:8050":
        ip_list.append({"ip":ip,"num":num})
        print(ip)
#    for block in ip_list:
#        print(block)
#        ip_new  = block['ip']
#        if ip != ip_new:
#            ip_list.append({"ip":ip,"num":num})
#    g.labels(info["host"]).set(info["info"]["current_head_block_number"])
now_time = datetime.datetime.now()
try_again = []
for chain in ip_list:
    print(now_time,chain["ip"],chain["num"])
    g.labels(chain["ip"],'mainnet').set(chain["num"])
    num=chain["num"]
    block_num=int(r.get('block_num'))
    if num and abs(block_num - num)>=2000:
        if chain["ip"].find("161.117.189.35")!=-1 or chain["ip"].find("115.171.44.123")!=-1 or chain["ip"].find("54.250.134.234")!=-1 or chain["ip"].find("223.72.141.97")!=-1:
            print("------------")
            print(chain['ip'],chain['num'])
            continue
        for region in region_list:
            if region.find(chain['ip']) !=-1:
                result=region
            else:
                result=chain['ip']
        print("==============error=======%s========================"%result)
        #send_msg("出块异常","获取出块节点异常%s,最大出块数%s,异常出块数%s"%(result,block_num,num))
        try_again.append(chain)
    print(num)
    list_nums.append(num)
    print("---------send to pushgateway--------------")
    push_to_gateway('10.22.0.11:9091', job='node_status', registry=registry)
max_num=max(list_nums)
r.set('block_num',max_num)
ws.close()

# test
try_again.append({'ip': '47.111.249.169:8050', 'num': 6427715})
if len(try_again):
    print("error message, try again...")
    print(try_again)
    count = 0
    i = 0
    while i < 3：
        i = i +1
        for peer in try_again:
            if peer["ip"].find("47.244.211.84") == -1:
                continue
            count = count + 1
            api_url = "ws://47.244.211.84:8701"
            print(api_url)
            num = get_ws_data("get_dynamic_global_properties", api_url)
            num = int(num)
            block_num=int(r.get('block_num'))
            if num and abs(block_num - num)<2000:
                break
            if num and count >= 3 and abs(block_num - num)>=2000:
                send_msg("出块异常","获取出块节点异常%s,最大出块数%s,异常出块数%s"%(result,block_num,num))
                print("==============error=======%s========================"%result)
        time.sleep(3)
    try_again = []
       

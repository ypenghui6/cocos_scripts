from datetime import datetime
import time

# 每n秒执行一次
def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        exec(open('get_lock_cocos_amount.py').read())
        time.sleep(n)
# 5s
timer(180)

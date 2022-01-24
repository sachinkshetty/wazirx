import configparser
import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests


class WazirxConnect:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('application.properties')
        self.wazirxApiKey = config.get('wazirx', 'wazirxApiKey')
        self.wazirxApiSecret = config.get('wazirx', 'wazirxApiSecret')

    def     cancel_existing_order(self, orderId):
        print("cancel_existing_order")
        apiUrl = "https://api.wazirx.com/sapi/v1/order"

        headers = self._get_headers(self.wazirxApiKey)

        delete_order_payload = self.delete_order_payload(orderId);
        encodedOrderPayload = urlencode(sorted(delete_order_payload.items()))
        signature = self.create_hmac_signature(encodedOrderPayload, self.wazirxApiSecret)
        delete_order_payload["signature"] = signature

        encodedDeleteOrderPayloadWithSignature = urlencode(sorted(delete_order_payload.items()))
        print(encodedDeleteOrderPayloadWithSignature)

        resp = requests.delete(apiUrl, data=encodedDeleteOrderPayloadWithSignature, headers=headers)
        return resp.status_code

    def get_existing_order(self):
        print("get_existing_order")

        apiUrl = "https://api.wazirx.com/sapi/v1/openOrders"

        headers = self._get_headers(self.wazirxApiKey)

        query_order_payload = self.query_order_payload();
        encodedOrderPayload = urlencode(sorted(query_order_payload.items()))
        signature = self.create_hmac_signature(encodedOrderPayload, self.wazirxApiSecret)
        query_order_payload["signature"] = signature

        encodedQueryOrderPayloadWithSignature = urlencode(sorted(query_order_payload.items()))

        resp = requests.get(apiUrl, data=encodedQueryOrderPayloadWithSignature, headers=headers)

        return resp

    def place_new_order(self, quantity, price):
        print("place_new_order")

        apiUrl = "https://api.wazirx.com/sapi/v1/order"

        headers = self._get_headers(self.wazirxApiKey)
        order_payload = self.create_order_payload(quantity, price);
        encodedOrderPayload = urlencode(sorted(order_payload.items()))
        signature = self.create_hmac_signature(encodedOrderPayload, self.wazirxApiSecret)
        order_payload["signature"] = signature

        encodedOrderPayloadWithSignature = urlencode(sorted(order_payload.items()))
        print(encodedOrderPayloadWithSignature)

        resp = requests.post(apiUrl, data=encodedOrderPayloadWithSignature, headers=headers)
        return resp

    def get_btc_market_price(self, crypto):
        print("get_btc_price")
        apiUrl = "https://api.wazirx.com/sapi/v1/ticker/24hr?symbol="+crypto
        resp = requests.get(apiUrl)
        print(resp.status_code)
        print(resp.json())
        return resp.json()['askPrice']


    def _get_headers(self,api_key):
        output = {"Content-Type": "application/x-www-form-urlencoded", "X-Api-Key": api_key}

        return output

    def create_order_payload(self,quantity,price):
        nonce = int(time.time()) * 1000
        print(nonce)
        payload_order = {"symbol": "btcinr", "side": "sell", "type": "limit", "quantity": quantity, "price": price,
                         "recvWindow": "60000", "timestamp": nonce}
        return payload_order

    def create_hmac_signature(self, encodedPayload, apisecret):
        signature = hmac.new(bytes(apisecret, 'latin-1'), bytes(encodedPayload, 'latin-1'),
                             digestmod=hashlib.sha256).hexdigest()
        return signature

    def query_order_payload(self):
        nonce = int(time.time()) * 1000
        print(nonce)
        payload_order = {"symbol": "btcinr", "recvWindow": "60000", "timestamp": nonce}
        return payload_order

    def delete_order_payload(self, orderId):
        nonce = int(time.time()) * 1000
        print(nonce)
        payload_order = {"symbol": "btcinr","orderId": orderId,"recvWindow": "60000", "timestamp": nonce}
        return payload_order

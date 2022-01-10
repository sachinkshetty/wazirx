import configparser
import hmac
import time
from urllib.parse import urlencode
from _sha256 import sha256
import decimal
import requests
from WazirxService import WazirxService


class PaxfulConnect:

    def __init__(self):
        self.tradeHashList = self.readTradeIdFromFile()
        self.wazirxservice = WazirxService()
        config = configparser.ConfigParser()
        config.read('application.properties')
        self.paxfulApiKey = config.get('wazirx', 'paxfulApiKey')
        self.paxfulApiSecret = config.get('wazirx', 'paxfulApiSecret')

    def start(self):
        while True:
            print("looping*********")
            self.connect()
            time.sleep(10)

    def connect(self):
        payload = self.createPayload(self.paxfulApiKey, self.paxfulApiSecret);
        url = "https://paxful.com/api/trade/list"
        resp = requests.post(url, data=payload, headers=self.createheaders())
        print(resp.status_code)
        print(resp.json())
        if 200 <= resp.status_code <= 202:
            if resp.json()['status'] == "success":
                trades = resp.json()['data']['trades']
                for trade in trades:
                    if trade['crypto_currency_code'] == 'BTC':
                        orderQuantity = float(trade['fiat_amount_requested']) / float(trade['fiat_price_per_crypto'])
                        orderQuantity = round(decimal.Decimal(orderQuantity), 5)
                        print(orderQuantity)
                        print(self.tradeHashList)
                        print(trade['trade_hash'])
                        if not self.tradeHashList.__contains__(trade['trade_hash']):
                            resp_status = self.wazirxservice.place_order(orderQuantity)
                            if 200 <= int(resp_status) <= 201:
                                self.tradeHashList.append(trade['trade_hash'])
                                print(self.tradeHashList)
                                self.writeTradeIdToFile(trade['trade_hash'])
            else:
                print("not able to get the trades")
                print(resp.json())
        else:
            print("response status code"+str(resp.status_code))


    def createPayload(self, apikey, apisecret):
        nonce = int(time.time())
        payload = {"apikey": apikey, "nonce": nonce}
        encodedPayload = urlencode(sorted(payload.items()))
        return encodedPayload + "&apiseal=" + self.createapiseal(encodedPayload, apisecret)

    def createapiseal(self, payload, apiSecret):
        return hmac.new(apiSecret.encode(), payload.encode(), sha256).hexdigest()

    def createheaders(self):
        return {"Accept": "application/json", "Content-Type": "text/plain"}

    def writeTradeIdToFile(self, tradeId):
        f = open("tradeId.txt", "a")
        f.write(tradeId + "\n")
        f.close()

    def readTradeIdFromFile(self):
        f = open("tradeId.txt", "r")
        tradeHash = f.read().splitlines()
        f.close()
        return tradeHash


if __name__ == '__main__':
    paxful = PaxfulConnect()
    paxful.start()
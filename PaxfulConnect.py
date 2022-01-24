import configparser
import hmac
import time
from urllib.parse import urlencode
from _sha256 import sha256
import decimal
import requests

from WazirxData import WazirxData
from WazirxService import WazirxService


class PaxfulConnect:

    def __init__(self):
        self.tradeHashList = self.readTradeIdFromFile()
        self.wazirxservice = WazirxService()
        self.wazirxData = WazirxData()
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
        print("paxful trade status : " + str(resp.status_code))
        # print(resp.json())
        if 200 <= resp.status_code <= 202:
            if resp.json()['status'] == "success":
                trades = resp.json()['data']['trades']
                for trade in trades:
                    if trade['crypto_currency_code'] == 'BTC' and trade['offer_type'] == 'buy':
                        orderQuantity = float(trade['fiat_amount_requested']) / float(trade['fiat_price_per_crypto'])
                        orderQuantity = str(round(decimal.Decimal(orderQuantity), 5))
                        print("orderQuantity : " + str(orderQuantity))
                        print(self.tradeHashList)
                        print(trade['trade_hash'])
                        tradeHash = trade['trade_hash']
                        if not self.tradeHashList.__contains__(trade['trade_hash']):
                            print("inserting order" + str(tradeHash))
                            # resp_status = self.wazirxservice.place_order_from_connect(orderQuantity, tradeHash)
                            self.wazirxData.insertorderquantity(orderQuantity, tradeHash)
                            self.tradeHashList.append(trade['trade_hash'])
                            self.writeTradeIdToFile(trade['trade_hash'])
                        else:
                            print("trade hash present in the hash file")
            else:
                print("not able to get the trades")
                print(resp.json())
        else:
            print("response status code" + str(resp.status_code))

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

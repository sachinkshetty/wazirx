import configparser
import json
import time

from WazirxData import WazirxData
from WazirxConnect import WazirxConnect


class WazirxService:

    def __init__(self):
        self.connect = WazirxConnect()
        config = configparser.ConfigParser()
        config.read('application.properties')
        self.threshold = config.get('wazirx', 'wazirxBtcThreshold')
        self.wazirxData = WazirxData()

    def place_order_from_connect(self, quantity, trade_hash):
        print("placing new order from connect: " + trade_hash)
        resp = self.connect.get_existing_order()
        print("existing order status : " + str(resp.status_code))
        return self.place_order(resp, quantity)

    def place_order(self, resp, quantity):
        print("placing new order")
        btcPrice = self.wazirxData.getPrice()
        print("btcPrice" + str(btcPrice))
        updatedBtcPrice = float(btcPrice) - float(self.threshold)
        if resp.status_code == 200:
            open_orders = resp.json()
            open_order_price = [open_order['price'] for open_order in open_orders]
            print(len(open_order_price))
            if len(open_orders) > 0:
                if float(open_order_price[0]) != btcPrice:
                    originalQuantity = [open_order['origQty'] for open_order in open_orders]
                    executedQuantity = [open_order['executedQty'] for open_order in open_orders]
                    orderId = [open_order['id'] for open_order in open_orders]
                    print(orderId[0])
                    cancelled_order_status = self.cancel_order(orderId[0])
                    print("cancelled resp status : " + str(cancelled_order_status))
                    if cancelled_order_status:
                        orderdetails = self.wazirxData.getorderdetails()
                        savedOrderQuantity = orderdetails[0]
                        tradeids = orderdetails[1]
                        updateOriginalQuantity = float(originalQuantity[0]) + float(savedOrderQuantity)
                        if float(executedQuantity[0]) > 0:
                            remainingOrderQuantity = updateOriginalQuantity - float(executedQuantity[0])
                            partialTradeId = str(orderId[0]) + "-Partial"
                            self.wazirxData.insertorderquantity(remainingOrderQuantity, partialTradeId)
                            tradeids = tradeids + "," + partialTradeId
                            updatedOrderQuantity = float(remainingOrderQuantity) + float(quantity)
                            print("updatedOrderQuantity : " + str(updatedOrderQuantity))
                        else:
                            updatedOrderQuantity = updateOriginalQuantity + float(quantity)
                            print("updatedOrderQuantity : " + str(updatedOrderQuantity))

                        return self.place_new_order(updatedBtcPrice, updatedOrderQuantity, tradeids)
                    else:
                        print("order id -- " + str(orderId[0]))
                        exit()
            else:
                return self.place_new_order_with_order_details(updatedBtcPrice)
        else:
            return resp.status_code

    def place_new_order_with_order_details(self, updatedBtcPrice):
        orderdetails = self.wazirxData.getorderdetails()
        savedOrderQuantity = orderdetails[0]
        print("savedOrderQuantity - " + str(savedOrderQuantity))
        tradeids = orderdetails[1]
        if savedOrderQuantity > 0:
            return self.place_new_order(updatedBtcPrice, savedOrderQuantity, tradeids)
        else:
            print("no order quantity present")

    def cancel_and_place_new_order(self, updatedBtcPrice, savedOrderQuantity, tradeids, orderId):
        status = self.cancel_order(orderId)
        if status:
            return self.place_new_order(updatedBtcPrice,savedOrderQuantity,tradeids)
        else:
            exit()

    def place_new_order(self, updatedBtcPrice, savedOrderQuantity, tradeids):
        orderResponse = self.connect.place_new_order(savedOrderQuantity, updatedBtcPrice)
        print(str(orderResponse.status_code) + " : order status code")
        orderResponseStatusCode = orderResponse.status_code
        if 200 <= orderResponseStatusCode <= 201:
            print(orderResponse.json()['id'])
            print("tradeIds : " + str(tradeids))
            self.wazirxData.updateorderquantity(orderResponse.json()['id'], tradeids)
        else:
            print("not able to place order")
        return orderResponse.status_code

    def cancel_order(self, orderId):
        while True:
            response = self.connect.cancel_existing_order(orderId)
            print("cancelled order response status : " + str(response.status_code))
            if response.status_code == 200:
                cancelled_order = json.loads(response.text)
                if "status" in cancelled_order:
                    print(cancelled_order['status'])
                    if cancelled_order['status'] != 'cancel':
                        time.sleep(5)
                    else:
                        return True
                else:
                    return False
            else:
                return False

    def place_order_from_updater(self, quantity):
        print("\n")
        print("----placing new order from updater: ")
        resp = self.connect.get_existing_order()
        print("existing order status : " + str(resp.status_code))
        if 200 <= int(resp.status_code) <= 201:
            print("existing order : " + str(resp.json()))
            return self.place_order(resp, quantity)

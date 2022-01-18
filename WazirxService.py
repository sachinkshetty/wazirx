import configparser

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
        print("existing order : " + str(resp.json()))
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
                    resp_status_code = self.connect.cancel_existing_order(orderId[0])
                    print("cancelled resp status : " + str(resp_status_code))
                    if resp_status_code == 200 or resp_status_code == 201:
                        savedOrderQuantity = self.wazirxData.getorderquantity()
                        updateOriginalQuantity = float(originalQuantity[0]) + float(savedOrderQuantity)
                        if float(executedQuantity[0]) > 0:
                            remainingOrderQuantity = updateOriginalQuantity - float(executedQuantity[0])
                            updatedOrderQuantity = float(remainingOrderQuantity) + float(quantity)
                            print("updatedOrderQuantity : " + str(updatedOrderQuantity))
                        else:
                            updatedOrderQuantity = updateOriginalQuantity + float(quantity)
                            print("updatedOrderQuantity : " + str(updatedOrderQuantity))

                        orderResponse = self.connect.place_new_order(updatedOrderQuantity, updatedBtcPrice)
                        print(str(orderResponse.status_code) + " : order status code")
                        orderResponseStatusCode = orderResponse.status_code
                        if 200 <= orderResponseStatusCode <= 201:
                            self.wazirxData.clearorderquantity()
                        else:
                            updatedOrderQuantity = updatedOrderQuantity - quantity
                            self.wazirxData.updateorderquantity(updatedOrderQuantity)

                        return orderResponse.status_code
            else:
                orderResponse = self.connect.place_new_order(quantity, updatedBtcPrice)
                print(str(orderResponse.status_code) + " : order status code")
                return orderResponse.status_code
        else:
            return resp.status_code

    def place_order_from_updater(self, quantity):
        print("placing new order from updater: ")
        resp = self.connect.get_existing_order()
        print("existing order status : " + str(resp.status_code))
        if 200 <= int(resp.status_code) <= 201:
            print("existing order : " + str(resp.json()))
            if len(resp.json()) > 0:
                return self.place_order(resp, quantity)

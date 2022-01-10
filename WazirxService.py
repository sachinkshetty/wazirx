import configparser

from PriceUpdate import PriceUpdate
from WazirxConnect import WazirxConnect


class WazirxService:

    def __init__(self):
        self.connect = WazirxConnect()
        config = configparser.ConfigParser()
        config.read('application.properties')
        self.threshold = config.get('wazirx', 'wazirxBtcThreshold')
        self.priceUpdate = PriceUpdate()

    def place_order(self, quantity):
        print("placing new order")
        resp = self.connect.get_existing_order()
        print("existing order : " + str(resp.json()) + "--" + str(resp.status_code))
        btcPrice = self.priceUpdate.getPrice()
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
                    print(type(resp_status_code))
                    if resp_status_code == 200 or resp_status_code == 201:
                        if float(executedQuantity[0]) > 0:
                            remainingOrderQuantity = float(originalQuantity[0]) - float(executedQuantity[0])
                            updatedOrderQuantity = float(remainingOrderQuantity) + float(quantity)
                        else:
                            updatedOrderQuantity = float(originalQuantity[0]) + float(quantity)
                        updatedOrderResponse = self.connect.place_new_order(updatedOrderQuantity, updatedBtcPrice)
                        print(str(updatedOrderResponse.status_code) + " : order status code")
                        return updatedOrderResponse.status_code
            else:
                orderResponse = self.connect.place_new_order(quantity, updatedBtcPrice)
                print(str(orderResponse.status_code) + " : order status code")
                return orderResponse.status_code
        else:
            return resp.status_code

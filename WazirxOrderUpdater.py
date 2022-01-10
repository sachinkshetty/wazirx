import time

from WazirxService import WazirxService


class WazixOrderUpdater:

    def __init__(self):
        self.service = WazirxService()

    def updateOrder(self):
        while True:
            self.service.place_order(0)
            time.sleep(2)

if __name__ == '__main__':
    orderUpdater = WazixOrderUpdater()
    orderUpdater.updateOrder()

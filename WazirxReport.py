from WazirxData import WazirxData


class WazirxReport:

    def __init__(self):
        self.data = WazirxData()

    def getreport(self):
        print("order to be processed : " + str(self.data.getOrderToBePlaced()))
        print("order processed : " + str(self.data.getOrderPlacedSucessfully()))
        print("order processed1 : " + str(self.data.getOrderPlacedSucessfully1()))
        # print("see all : ") + str(self.data.getall())


if __name__ == '__main__':
    report = WazirxReport()
    report.getreport()

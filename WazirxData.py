import sqlite3


class WazirxData:
    def __init__(self):
        self.con = sqlite3.connect('cryptoPrice.db')
        self.cur = self.con.cursor()

        # Create table
        self.cur.execute('''CREATE TABLE  IF NOT EXISTS crypto_price
                       (price)''')
        self.cur.execute('''CREATE TABLE  IF NOT EXISTS crypto_order_quantity
                             (tradeId, order_quantity, orderId)''')

    def update(self, price):
        print(price)
        # val = price
        # self.cur.execute("REPLACE INTO crypto_price(price) VALUES (%s)", val)
        sql = "DELETE FROM crypto_price"
        self.cur.execute(sql)
        sql = "REPLACE INTO crypto_price(price) VALUES (" + price + ")"
        self.cur.execute(sql)
        self.con.commit()

    def getPrice(self):
        for row in self.cur.execute('SELECT price FROM crypto_price'):
            return row[0]

    def updateorderquantity(self, quantity):
        print(quantity)
        # val = price
        # self.cur.execute("REPLACE INTO crypto_price(price) VALUES (%s)", val)
        sql = "REPLACE INTO crypto_order_quantity(order_quantity) VALUES (" + str(quantity) + ")"
        self.cur.execute(sql)
        self.con.commit()

    def clearorderquantity(self):
        sql = "DELETE FROM crypto_order_quantity"
        self.cur.execute(sql)
        self.con.commit()

    def getorderdetails(self):
        print("get order quantity")
        orderquantity = 0
        tradeid = ""
        orderdetails = []
        for row in self.cur.execute('SELECT order_quantity, tradeId FROM crypto_order_quantity where orderId '
                                    'is Null'):
            orderquantity += float(row[0])
            tradeid += row[1] + ","
        tradeid = tradeid.rstrip(",")
        orderdetails.insert(0, orderquantity)
        orderdetails.insert(1, tradeid)
        return orderdetails

    def test(self):
        self.cur.execute('SELECT * FROM crypto_order_quantity where orderId '
                         'is Null')
        print(self.cur.fetchall())

    def test1(self):
        self.cur.execute('SELECT * FROM crypto_order_quantity where orderId '
                         'is not Null')
        print(self.cur.fetchall())

    def insertorderquantity(self, quantity, tradeId):
        sql = "INSERT INTO crypto_order_quantity(tradeId, order_quantity,orderId) VALUES (?,?,?) "
        self.cur.execute(sql, (tradeId, quantity, None))
        self.con.commit()

    def updateorderquantity(self, orderId, tradeids):
        print(tradeids)
        for tradeid in tradeids.split(","):
            sql = "update crypto_order_quantity set orderId = ? where tradeId = ?"
            self.cur.execute(sql, (orderId, tradeid))
            self.con.commit()


# if __name__ == '__main__':
#     orderUpdater = WazirxData()
#     orderUpdater.insertorderquantity(1, "dsdsd")
#     orderUpdater.insertorderquantity(1, "s12121")
#     orderUpdater.insertorderquantity(1, "fdfffgf")
#     order = orderUpdater.getorderdetails()
#     orderUpdater.updateorderquantity("1111111", order[1])
#     orderUpdater.test1()
#     orderUpdater.test()


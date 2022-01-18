import sqlite3


class WazirxData:
    def __init__(self):
        self.con = sqlite3.connect('cryptoPrice.db')
        self.cur = self.con.cursor()

        # Create table
        self.cur.execute('''CREATE TABLE  IF NOT EXISTS crypto_price
                       (price)''')
        self.cur.execute('''CREATE TABLE  IF NOT EXISTS crypto_order_quantity
                             (order_quantity)''')

    def update(self, price):
        print(price)
        # val = price
        # self.cur.execute("REPLACE INTO crypto_price(price) VALUES (%s)", val)
        sql = "DELETE FROM crypto_price"
        self.cur.execute(sql)
        sql = "REPLACE INTO crypto_price(price) VALUES ("+price+")"
        self.cur.execute(sql)
        self.con.commit()

    def getPrice(self):
        for row in self.cur.execute('SELECT price FROM crypto_price'):
            return row[0]

    def updateorderquantity(self, quantity):
        print(quantity)
        # val = price
        # self.cur.execute("REPLACE INTO crypto_price(price) VALUES (%s)", val)
        sql = "INSERT INTO crypto_order_quantity(order_quantity) VALUES ("+quantity+")"
        self.cur.execute(sql)
        self.con.commit()

    def clearorderquantity(self):
        sql = "DELETE FROM crypto_order_quantity"
        self.cur.execute(sql)
        self.con.commit()

    def getorderquantity(self):
        print("get order quantity")
        orderquantity = 0
        for row in self.cur.execute('SELECT order_quantity FROM crypto_order_quantity'):
            print(row[0])
            orderquantity = row[0]
        return orderquantity



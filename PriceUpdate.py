import sqlite3


class PriceUpdate:
    def __init__(self):
        self.con = sqlite3.connect('cryptoPrice.db')
        self.cur = self.con.cursor()

        # Create table
        self.cur.execute('''CREATE TABLE  IF NOT EXISTS crypto_price
                       (price)''')

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



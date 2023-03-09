import sqlite3

class WiFiPentestToolDB:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cracking_data
                            (Bssid TEXT PRIMARY KEY,
                             signal_strength INT(3),
                             channel INT(3),
                             encryption TEXT)""")
        self.conn.commit()

    def insert_data(self, bssid, signal_strength, channel, encryption):
        self.cur.execute("INSERT INTO cracking_data VALUES (?, ?, ?, ?)", (bssid, signal_strength, channel, encryption))
        self.conn.commit()

    def delete_data(self, bssid):
        self.cur.execute("DELETE FROM cracking_data WHERE Bssid=?", (bssid,))
        self.conn.commit()

    def get_all_data(self):
        self.cur.execute("SELECT * FROM cracking_data")
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()

# create a database object
db = WiFiPentestToolDB('WiFiPentestTool.db')

# insert data into the database
db.insert_data('BC:2C:12:AC:AD:A8', 98, 2, 'WPA2')

# delete data from the database
db.delete_data('BC:2C:12:AC:AD:A8')

# get all data from the database
rows = db.get_all_data()
print(rows)

from SQL import WifiDatabase

# Create an instance of the Database class
db = WifiDatabase()

# Call methods of the instance to perform database operations
db.create_table()
db.insert_data()
db.update_data()
db.delete_data()
db.get_all_data()

network = ['BC:2C:12:AC:AD:A8', 98, 2, 'WPA2']
db.insert_data(*network)

bssid = 'BC:2C:12:AC:AD:A8'
new_signal_strength = 100
db.update_data(bssid, new_signal_strength)
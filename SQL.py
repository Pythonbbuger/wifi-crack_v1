import sqlite3
import time
import datetime


class WifiDatabase:

    BSSID = 0
    START = 1
    database_data_list = list()

    def __init__(self):
        self.conn = sqlite3.connect('WiFiPentestTool.db')
        self.create_cracking_data_table()

    def create_cracking_data_table(self):
        create_table_query_1 = """
                                  CREATE TABLE IF NOT EXISTS cracking_data 
                                  (
                                    Bssid TEXT PRIMARY KEY,
                                    signal_strength int(3),
                                    channel int(3),
                                    encryption TEXT
                                  )
                               """
        create_table_query_2 = """
                                  CREATE TABLE IF NOT EXISTS client 
                                  (
                                     client_id int,
                                     client_username TEXT,
                                     client_pw TEXT,
                                     AP_role TEXT,
                                     last_seen datetime,
                                     Bssid TEXT,
                                     PRIMARY KEY(client_id, Bssid),
                                     FOREIGN KEY(Bssid) REFERENCES cracking_data(Bssid)
                                  )
                               """
        cursor = self.conn.cursor()
        cursor.execute(create_table_query_1)
        cursor.execute(create_table_query_2)
        self.conn.commit()

    def create_record(self, ssid, signal_strength, channel, encryption):
        insert_query = "INSERT OR IGNORE INTO cracking_data VALUES(?, ?, ?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(insert_query, (ssid, signal_strength, channel, encryption))
        self.conn.commit()

    def update_record(self, ssid, crack_time):
        query = "UPDATE cracking_data set crack_time = ? where Bssid = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (ssid, crack_time))
        self.conn.commit()

    def delete_record(self, ssid):
        query = "DELETE FROM cracking_data where Bssid = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (ssid,))
        self.conn.commit()

    import sqlite3

    def delete_data(bssid):
        # Connect to the database
        conn = sqlite3.connect('WiFiPentestTool.db')
        c = conn.cursor()

        # Execute the DELETE statement with the given Bssid value
        c.execute("DELETE FROM cracking_data WHERE Bssid = ?", (bssid,))

        # Commit the transaction and close the cursor and connection
        conn.commit()
        c.close()
        conn.close()


    def get_all_records(self):
        query = "SELECT * FROM cracking_data"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

import sqlite3

def create_table():
    # Connect to the database
    conn = sqlite3.connect('WiFiPentestTool.db')

    # Create a cursor object
    c = conn.cursor()

    # Create a new table
    c.execute('''CREATE TABLE cracking_data
                 (Bssid TEXT PRIMARY KEY,
                  signal_strength INT(3),
                  channel INT(3),
                  encryption TEXT)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_data(Bssid, signal_strength, channel, encryption):
    # Connect to the database
    conn = sqlite3.connect('WiFiPentestTool.db')

    # Create a cursor object
    c = conn.cursor()

    # Insert a row of data into the table
    c.execute("INSERT INTO cracking_data (Bssid, signal_strength, channel, encryption) VALUES (?, ?, ?, ?)",
              (Bssid, signal_strength, channel, encryption))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
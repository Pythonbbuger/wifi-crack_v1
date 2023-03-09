import sqlite3

class APdatabase:
    def __init__(self):
        self.conn = sqlite3.connect('APTool.db')
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS AP_data (
                            Bssid TEXT PRIMARY KEY,
                            SSID TEXT,
                            signal_strength INT(3),
                            channel INT(3),
                            encryption TEXT,
                            Password TEXT,
                            scan_time TEXT
                            )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS AP_Client_data (
                            Bssid TEXT PRIMARY KEY,
                            AP_Role TEXT,
                            AP_MACAddress TEXT,
                            Last_seen TEXT,
                            Client_name TEXT,
                            FOREIGN KEY (Bssid) REFERENCES AP_data(Bssid)
                            )''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def update_ap_data(self, bssid, ssid, signal_strength, channel, encryption, password):
        self.c.execute("SELECT * FROM AP_data WHERE Bssid = ?", (bssid,))
        existing_row = self.c.fetchone()
        if existing_row:
            self.c.execute("UPDATE AP_data SET SSID = ? signal_strength = ?, channel = ?, encryption = ? ,Password = ? ,WHERE Bssid = ?", (ssid, signal_strength, channel, encryption, password, bssid))
        else:
            self.c.execute("INSERT INTO AP_data (Bssid, SSID, signal_strength, channel, encryption, Password) VALUES (?, ?, ?, ?, ?, ?)", (bssid, ssid, signal_strength, channel, encryption, password))
        self.conn.commit()

    def update_ap_client_data(self, bssid, ap_role, ap_mac_address, last_seen, client_name):
        self.c.execute("SELECT * FROM AP_Client_data WHERE Bssid = ?", (bssid,))
        existing_row = self.c.fetchone()
        if existing_row:
            self.c.execute("UPDATE AP_Client_data SET AP_Role = ?, AP_MACAddress = ?, Last_seen = ?, Client_name = ? WHERE Bssid = ?", (ap_role, ap_mac_address, last_seen, client_name, bssid))
        else:
            self.c.execute("INSERT INTO AP_Client_data (Bssid, AP_Role, AP_MACAddress, Last_seen, Client_name) VALUES (?, ?, ?, ?, ?)", (bssid, ap_role, ap_mac_address, last_seen, client_name))
        self.conn.commit()

    def delete(self, table_name, bssid):
        if table_name == "AP_data":
            self.c.execute("DELETE FROM AP_data WHERE Bssid = ?", (bssid,))
        elif table_name == "AP_Client_data":
            self.c.execute("DELETE FROM AP_Client_data WHERE Bssid = ?", (bssid,))
        else:
            print("Invalid table name")
            return
        self.conn.commit()

# Create an instance of the APdatabase class
apdb = APdatabase()

# Delete a row from the AP_data table based on Bssid
bssid_to_delete = '01:23:45:67:89:AB'
apdb.delete("AP_data", bssid_to_delete)

# Delete a row from the AP_Client_data table based on Bssid
bssid_to_delete = '01:23:45:67:89:AB'
apdb.delete("AP_Client_data", bssid_to_delete)
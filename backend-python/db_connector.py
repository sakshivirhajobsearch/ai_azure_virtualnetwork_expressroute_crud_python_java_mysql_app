import mysql.connector
from mysql.connector import Error
import configparser

# Load config
config = configparser.ConfigParser()
config.read('config.properties')

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=config.get('DEFAULT', 'mysql_host'),
        user=config.get('DEFAULT', 'mysql_user'),
        password=config.get('DEFAULT', 'mysql_password'),
        database=config.get('DEFAULT', 'mysql_db')
    )
    cursor = conn.cursor()
    print("Connected to MySQL successfully.")
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit(1)

# Auto-create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS virtual_networks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255),
    address_space VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expressroutes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    peering_location VARCHAR(255),
    bandwidth VARCHAR(255)
)
""")
conn.commit()

# ----------------- CRUD Operations -----------------
def insert_virtual_network(name, location, address_space):
    cursor.execute(
        "INSERT INTO virtual_networks (name, location, address_space) VALUES (%s, %s, %s)",
        (name, location, address_space)
    )
    conn.commit()

def fetch_virtual_networks():
    cursor.execute("SELECT * FROM virtual_networks")
    return cursor.fetchall()

def update_virtual_network(vnet_id, name=None, location=None, address_space=None):
    sql = "UPDATE virtual_networks SET "
    params = []
    updates = []
    if name:
        updates.append("name=%s")
        params.append(name)
    if location:
        updates.append("location=%s")
        params.append(location)
    if address_space:
        updates.append("address_space=%s")
        params.append(address_space)
    if not updates:
        return
    sql += ", ".join(updates) + " WHERE id=%s"
    params.append(vnet_id)
    cursor.execute(sql, tuple(params))
    conn.commit()

def delete_virtual_network(vnet_id):
    cursor.execute("DELETE FROM virtual_networks WHERE id=%s", (vnet_id,))
    conn.commit()

def insert_expressroute(name, peering_location, bandwidth):
    cursor.execute(
        "INSERT INTO expressroutes (name, peering_location, bandwidth) VALUES (%s, %s, %s)",
        (name, peering_location, bandwidth)
    )
    conn.commit()

def fetch_expressroutes():
    cursor.execute("SELECT * FROM expressroutes")
    return cursor.fetchall()

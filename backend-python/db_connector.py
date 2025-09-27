import mysql.connector

# ---------------- MySQL Connection Helper ----------------
def get_connection(host, user, password, database):
    return mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )

# ---------------- FETCH Operations ----------------
def fetch_vnets(host, user, password, database):
    conn = get_connection(host, user, password, database)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM virtual_networks")  # Replace with your table name
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def fetch_expressroutes(host, user, password, database):
    conn = get_connection(host, user, password, database)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM expressroutes")  # Replace with your table name
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# ---------------- INSERT Operations ----------------
def insert_vnet(host, user, password, database, vnet_data):
    conn = get_connection(host, user, password, database)
    try:
        cursor = conn.cursor()
        cols = ", ".join(vnet_data.keys())
        vals = ", ".join(["%s"] * len(vnet_data))
        sql = f"INSERT INTO virtual_networks ({cols}) VALUES ({vals})"
        cursor.execute(sql, list(vnet_data.values()))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def insert_expressroute(host, user, password, database, er_data):
    conn = get_connection(host, user, password, database)
    try:
        cursor = conn.cursor()
        cols = ", ".join(er_data.keys())
        vals = ", ".join(["%s"] * len(er_data))
        sql = f"INSERT INTO expressroutes ({cols}) VALUES ({vals})"
        cursor.execute(sql, list(er_data.values()))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

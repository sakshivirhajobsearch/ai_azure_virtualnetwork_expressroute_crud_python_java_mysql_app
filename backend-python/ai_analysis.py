import configparser
from db_connector import fetch_vnets, fetch_expressroutes

# === Load configuration ===
config = configparser.ConfigParser()
files_read = config.read('config.properties')
if not files_read:
    raise FileNotFoundError("config.properties not found in current directory.")

# Debug: check sections
print("Config Sections:", config.sections())  # Should include 'mysql' and 'azure'

# MySQL config
mysql_host = config['mysql']['mysql_host']
mysql_user = config['mysql']['mysql_user']
mysql_password = config['mysql']['mysql_password']
mysql_db = config['mysql']['mysql_db']

# === Fetch Virtual Networks from MySQL ===
print("\nFetching Virtual Networks from database...")
vnets = fetch_vnets(mysql_host, mysql_user, mysql_password, mysql_db)
for vnet in vnets:
    print(vnet)

# === Fetch ExpressRoute connections from MySQL ===
print("\nFetching ExpressRoute connections from database...")
expressroutes = fetch_expressroutes(mysql_host, mysql_user, mysql_password, mysql_db)
for er in expressroutes:
    print(er)

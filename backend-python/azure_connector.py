import configparser
import sys
from db_connector import insert_vnet, insert_expressroute
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import ClientAuthenticationError

# === Load configuration ===
config = configparser.ConfigParser()
files_read = config.read('config.properties')
if not files_read:
    raise FileNotFoundError("config.properties not found in current directory.")

# MySQL config
mysql_host = config['mysql']['mysql_host'].strip()
mysql_user = config['mysql']['mysql_user'].strip()
mysql_password = config['mysql']['mysql_password'].strip()
mysql_db = config['mysql']['mysql_db'].strip()

# Azure config
tenant_id = config['azure']['tenant_id'].strip()
client_id = config['azure']['client_id'].strip()
client_secret = config['azure']['client_secret'].strip()
subscription_id = config['azure']['subscription_id'].strip()

# === Authenticate to Azure ===
try:
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    # Test credential by requesting a token
    token = credential.get_token("https://management.azure.com/.default")
    print("Azure authentication successful.")
except ClientAuthenticationError as e:
    print(f"Authentication failed. Check tenant_id, client_id, client_secret.\nError: {e}")
    sys.exit(1)
except ValueError as e:
    print(f"Invalid tenant ID or other config value.\nError: {e}")
    sys.exit(1)

network_client = NetworkManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

# === Fetch Virtual Networks from Azure and insert into MySQL ===
def sync_vnets_to_db(resource_group_name):
    try:
        vnets = network_client.virtual_networks.list(resource_group_name)
        for vnet in vnets:
            vnet_data = {
                "name": vnet.name,
                "location": vnet.location,
                "address_space": ",".join(vnet.address_space.address_prefixes),
                "resource_group": resource_group_name
            }
            insert_vnet(mysql_host, mysql_user, mysql_password, mysql_db, vnet_data)
            print(f"Inserted VNet '{vnet.name}' from RG '{resource_group_name}' into MySQL.")
    except Exception as e:
        print(f"Error syncing VNets for resource group '{resource_group_name}': {e}")

# === Fetch ExpressRoute circuits from Azure and insert into MySQL ===
def sync_expressroutes_to_db(resource_group_name):
    try:
        expressroutes = network_client.express_route_circuits.list_by_resource_group(resource_group_name)
        for er in expressroutes:
            er_data = {
                "name": er.name,
                "location": er.location,
                "service_provider": er.service_provider_properties.service_provider_name if er.service_provider_properties else None,
                "bandwidth": er.service_provider_properties.bandwidth_in_mbps if er.service_provider_properties else None,
                "resource_group": resource_group_name
            }
            insert_expressroute(mysql_host, mysql_user, mysql_password, mysql_db, er_data)
            print(f"Inserted ExpressRoute '{er.name}' from RG '{resource_group_name}' into MySQL.")
    except Exception as e:
        print(f"Error syncing ExpressRoutes for resource group '{resource_group_name}': {e}")

# === Main execution: loop through all resource groups ===
if __name__ == "__main__":
    try:
        resource_groups = resource_client.resource_groups.list()
        for rg in resource_groups:
            rg_name = rg.name
            print(f"\nSyncing resources from resource group: {rg_name}")
            sync_vnets_to_db(rg_name)
            sync_expressroutes_to_db(rg_name)
        print("\nAzure sync to MySQL completed successfully.")
    except Exception as e:
        print(f"Error fetching resource groups: {e}")
        sys.exit(1)

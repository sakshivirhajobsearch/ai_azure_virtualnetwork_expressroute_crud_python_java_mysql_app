from db_connector import (
    insert_virtual_network,
    insert_expressroute,
    fetch_virtual_networks,
    fetch_expressroutes,
    update_virtual_network,
    delete_virtual_network
)

# ---------------- Insert Dummy Virtual Networks ----------------
insert_virtual_network('VNet-Test-1', 'East US', '10.0.0.0/16')
insert_virtual_network('VNet-Test-2', 'West Europe', '192.168.1.0/24')
insert_virtual_network('VNet-Test-3', 'Southeast Asia', '172.16.0.0/12')

# ---------------- Insert Dummy ExpressRoutes ----------------
insert_expressroute('ER-Test-1', 'Equinix Ashburn', '1Gbps')
insert_expressroute('ER-Test-2', 'London Docklands', '10Gbps')
insert_expressroute('ER-Test-3', 'Singapore', '2Gbps')

# ---------------- Display ----------------
print("Virtual Networks:")
for v in fetch_virtual_networks():
    print(v)

print("\nExpressRoutes:")
for er in fetch_expressroutes():
    print(er)

# ---------------- Update/Delete Example ----------------
update_virtual_network(1, location='Central US')
delete_virtual_network(3)

print("\nVirtual Networks after update/delete:")
for v in fetch_virtual_networks():
    print(v)

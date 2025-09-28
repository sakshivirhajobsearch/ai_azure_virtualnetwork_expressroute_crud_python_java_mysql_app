from db_connector import fetch_virtual_networks, fetch_expressroutes

# Simple "AI" example: count VNets per location
vnets = fetch_virtual_networks()
location_count = {}
for v in vnets:
    loc = v[2]
    location_count[loc] = location_count.get(loc, 0) + 1

print("Virtual Networks per location:")
for loc, count in location_count.items():
    print(f"{loc}: {count}")

# Count ExpressRoutes per bandwidth
ers = fetch_expressroutes()
bandwidth_count = {}
for er in ers:
    bw = er[3]
    bandwidth_count[bw] = bandwidth_count.get(bw, 0) + 1

print("\nExpressRoutes per bandwidth:")
for bw, count in bandwidth_count.items():
    print(f"{bw}: {count}")

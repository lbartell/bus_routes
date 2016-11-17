from BusRouteAnalysis import *

# Example instance
kwargs = {'route_number': 10}
route = BusRoute(**kwargs)
#route.show_route()

# Find minimum walking time to get to the bus
pointA = '102 W Falls St, Ithaca, NY'
pointB = route.coordinates[:,1::-1].tolist()
dist, time = distance_time(pointA, pointB)
ix = time[0].index(min(time[0]))
print 'Minimum time is %d sec, to (%f, %f)'%(min(time[0]), pointB[ix][0], pointB[ix][1])


## Dict of multiple routes
#bus_numbers = (10, 36, 15)
#routes = get_routes(bus_numbers)
#
#my_address = '102 W Falls St, Ithaca, NY'
#my_coords = geocode(my_address)
#print my_coords

## Example distance calculation
#dist, dur = distance_time(('Ithaca, NY', 'Ithaca, NY'), ('New York City', 'Lansing, NY'), printout=True)




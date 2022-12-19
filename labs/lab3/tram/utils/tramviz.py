from .trams import readTramNetwork, get_path_cost, specialize_stops_to_lines, specialized_geo_distance, specialized_transition_time
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
from django.conf import settings


# helper function to return the shortest path, based on either distance or time
def optimal_path_finder(tramnetwork, dep, dest, geo_dist=False):
    spec_tram = specialize_stops_to_lines(tramnetwork)

    # all vertices that contain dep
    deps = list(map(lambda line: (dep, line), tramnetwork.stop_lines(dep)))
    # all vertices that contain dest
    dests = list(map(lambda line: (dest, line), tramnetwork.stop_lines(dest)))

    def calc_transition_time(a, b):
        return specialized_transition_time(spec_tram, a, b)

    def calc_geo_distance(x, y):
        return specialized_geo_distance(spec_tram, x, y)

    # to determine if distance or time
    shortest_type = calc_transition_time
    if geo_dist:
        shortest_type = calc_geo_distance

    # the returning shortest or quickest path
    optimal_path = []
    # the cost of the optimal path, initially infinity
    optimal_path_cost = float('inf')

    # loop to know which line in dep is best to take, and which line in dest is best to arrive to
    for dep_node in deps:
        for dest_node in dests:
            current_path = dijkstra(spec_tram, dep_node, shortest_type)[dest_node]
            current_path_cost = get_path_cost(spec_tram, current_path, geo_dist)
            # compare the current path with the optimal path
            if  current_path_cost < optimal_path_cost:
                # update optimal path cost
                optimal_path_cost = current_path_cost
                # update optimal path
                optimal_path = current_path

            #print(current_path)
            #print(current_path_cost)
            #print('\n')

    return optimal_path, optimal_path_cost


def show_shortest(dep, dest):
    network = readTramNetwork()

    def convert_tram_nodes(optimal_path):
        return [v[0] for v in optimal_path]

    # find the quickest
    quickest = optimal_path_finder(network, dep, dest)
    # find the shortest
    shortest = optimal_path_finder(network, dep, dest, geo_dist=True)
    # get the quickest path description
    quickest_path = convert_tram_nodes(quickest[0])
    # get the shortest path description
    shortest_path = convert_tram_nodes(shortest[0])
    # get the quickest path cost
    quickest_cost = quickest[1]
    # get shortest path cost
    shortest_cost = shortest[1]

    def colors(v):
        if v in shortest_path and v in quickest_path:
            return 'cyan'
        elif v in shortest_path:
            return 'green'
        elif v in quickest_path:
            return 'orange'
        else:
            return 'white'

    timepath = 'Quickest: ' + ', '.join(quickest_path) + './  ' + str(quickest_cost) + ' minutes'
    geopath = 'Shortest: ' + ', '.join(shortest_path) + './  ' + str(shortest_cost) + ' km'

    color_svg_network(colormap=colors)

    return timepath, geopath



#print("\noptimal path: " + str(optimal_path_finder(readTramNetwork(), 'Rymdtorget Spårvagn', 'Långedrag')))
#print("\noptimal path: " + str(optimal_path_finder(readTramNetwork(), 'Rymdtorget Spårvagn', 'Långedrag', geo_dist=True)))

#print("\noptimal path: " + str(optimal_path_finder(readTramNetwork(), 'Chalmers', 'Valand', geo_dist=True)))



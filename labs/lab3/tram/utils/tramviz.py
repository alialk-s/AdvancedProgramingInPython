from .trams import readTramNetwork, get_path_cost, specialize_stops_to_lines, specialized_geo_distance, specialized_transition_time
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings

# baseline tram visualization for Lab 3
# creates by default an SVG image usable on the home page
# this image can then be coloured by using tramviz.py, which operates directly on the SVG file
# you don't need to use this file unless you want to use your own gbg_tramnet.svg
# this will be needed in Bonus task 2, where you change the URLs of vertices
# but you should only do this once, not every time you display a route
# rename the resulting file to gbg_tramnet.svg when you have your final version


def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network = readTramNetwork()

    # TODO: replace this mock-up with actual computation using dijkstra.
    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    #
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.

    def convert_tram_nodes(optimal_path):
        return [v[0] for v in optimal_path]

    quickest = convert_tram_nodes(optimal_path_finder(network, dep, dest))
    shortest = convert_tram_nodes(optimal_path_finder(network, dep, dest, geo_dist=True))

    def colors(v):
        if v in shortest and v in quickest:
            return 'cyan'
        elif v in shortest:
            return 'green'
        elif v in quickest:
            return 'orange'
        else:
            return 'white'

    timepath = 'The quickest route from ' + dep + ' to ' + dest + ': ' + str(quickest)
    geopath = 'The shortest route from ' + dep + ' to ' + dest + ': ' + str(shortest)

    color_svg_network(colormap=colors)

    return timepath, geopath


# helper function to return the shortest path, based on either distance or time
def optimal_path_finder(tramnetwork, dep, dest, geo_dist = False):
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

    # loop to know which line in dep to which line in dest are best
    for dep_node in deps:
        for dest_node in dests:
            path = dijkstra(spec_tram, dep_node, shortest_type)[dest_node]
            path_cost = get_path_cost(spec_tram, path, geo_dist)
            # compare the current path with the optimal path
            if  path_cost < optimal_path_cost:
                # update optimal path cost
                optimal_path_cost = path_cost
                # update optimal path
                optimal_path = path

            #print(path)
            #print(get_path_cost(spec_tram, path))
            #print('\n')

    return optimal_path


#if __name__ == '__main__':
 #   network = readTramNetwork()
    #network_graphviz(network)
#
print("\noptimal path: " + str(optimal_path_finder(readTramNetwork(), 'Friskväderstorget', 'Hinsholmen')))
#from bs4 import BeautifulSoup
#import requests
#import re

#vasttrafik_url = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'
#doc = BeautifulSoup(requests.get(vasttrafik_url).text, 'html.parser')
#print(doc)
#print(doc.find(text=re.compile('Chalmers')).parent['href'].split('/')[1])

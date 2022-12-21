import csv
import matplotlib.pyplot as plt
import networkx as nx
from haversine import haversine
from matplotlib.collections import LineCollection
import time

from networkx import algorithms

AIRPORTS_FILE = 'airports.dat'
ROUTS_FILE = 'routes.dat'

def read_file(file):
    with open(file, 'r', encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter='\t')
        data = [row for row in rows]
    return data

def remove_quotation_marks(name):
    if name[0] == '"' and name[len(name) - 1] == '"':
        return name[1: len(name) - 1]
    else:
        return name


def mk_airportdict(aFILE=AIRPORTS_FILE):
    #start_time = time.time()
    data = read_file(aFILE)
    airport_dict = {}
    for line in data:
        datastr = line[0]
        temp_list = datastr.split(',')
        try:
            value_dict = {'name': remove_quotation_marks(temp_list[1]), 'city': remove_quotation_marks(temp_list[2]),
                          'country': remove_quotation_marks(temp_list[3]), 'IATA': remove_quotation_marks(temp_list[4]),
                          'ICAO': remove_quotation_marks(temp_list[5]), 'lat': float(temp_list[6]),
                          'lon': float(temp_list[7]),
                          'altitude': float(temp_list[8]), 'timezone': float(temp_list[9]),
                          'DST': remove_quotation_marks(temp_list[10]), 'TZ': remove_quotation_marks(temp_list[11]),
                          'type': remove_quotation_marks(temp_list[12]),
                          'source': remove_quotation_marks(temp_list[13])}
            airport_dict[int(temp_list[0])] = value_dict
        # just skip any line with unstructured data
        except:
            continue

    #print("--- %s seconds ---" % (time.time() - start_time))
    return airport_dict

def mk_routeset(rFILE=ROUTS_FILE):
    data = read_file(rFILE)
    routs_set = set()

    for line in data:
        datastr = line[0]
        try:
            temp_list = datastr.split(',')
            pair = (int(temp_list[3]), int(temp_list[5]))
            routs_set.add(pair)
        except ValueError:
            continue

    return routs_set



def mk_routegraph(routeset):
    # graph for storing airports as nodes and routes as edges
    g = nx.Graph()
    # all retrieved airports
    airports = mk_airportdict()
    for pair in routeset:
        # id of first airport in the tuple
        id1 = pair[0]
        # id of second airport in tuple
        id2 = pair[1]
        # due to the unstructured data
        if id1 in airports and id2 in airports:
            # lat and lon for the first airport
            lat1, lon1 = airports[id1]['lat'], airports[id1]['lon']
            # lat and lon for the second airport
            lat2, lon2 = airports[id2]['lat'], airports[id2]['lon']
            # first airport's geographical point
            p1 = (lat1, lon1)
            # second airport's geographical point
            p2 = (lat2, lon2)
            # distance between them
            distance = haversine(p1, p2)
            # add a weighted edge between them
            g.add_edge(id1, id2, weight=distance)

    return g

def airports():
    airports = mk_airportdict()
    points = []
    for a in airports:
        # x corresponds to a point's lon and y corresponds to a point's lat
        x, y = airports[a]['lon'], airports[a]['lat']
        # add them as a single point to the list
        points.append((x, y))

    plt.scatter(*zip(*points), edgecolors='blue', s=0.2)
    plt.show()

def routes():
    start_time = time.time()
    g = mk_routegraph(mk_routeset())
    airport_dict = mk_airportdict()
    edges = g.edges
    lines = []
    for pair in edges:
        lat1, lon1 = airport_dict[pair[0]]['lat'], airport_dict[pair[0]]['lon']
        lat2, lon2 = airport_dict[pair[1]]['lat'], airport_dict[pair[1]]['lon']
        point1 = (lon1, lat1)
        point2 = (lon2, lat2)
        lines.append([point1, point2])

    lc = LineCollection(lines, colors=['blue', 'gray', 'red', 'green'], linewidths=0.15)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.add_collection(lc)
    x = [i[0] for j in lines for i in j]
    y = [i[1] for j in lines for i in j]

    ax1.scatter(x, y, s=0.1)
    print("--- %s seconds ---" % (time.time() - start_time))

    plt.show()


def k_spanning_tree(G, k=1000):
    start_time = time.time()
    MST = list(algorithms.tree.mst.minimum_spanning_edges(G))
    weights = [MST[i][2]['weight'] for i in range(len(MST))]

    for j in range(k - 1):
        # get index of the the edge with max weight
        index_max = weights.index(max(weights))
        # remove that edge from the list
        del MST[index_max]
        # remove the weight from weights for updating index_max
        del weights[index_max]

    # create new graph with the remaining edges
    new_G = nx.Graph(MST)
    print("--- %s seconds ---" % (time.time() - start_time))

    return new_G


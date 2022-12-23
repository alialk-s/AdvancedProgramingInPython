import csv
import sys
import networkx as nx
from haversine import haversine
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from sklearn.cluster import KMeans

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


def mk_routegraph(routeset=mk_routeset()):
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


def airports_as_points():
    airports = mk_airportdict()
    points = []
    for a in airports:
        # x corresponds to a point's lon and y corresponds to a point's lat
        x, y = airports[a]['lon'], airports[a]['lat']
        # add them as a single point to the list
        points.append((x, y))

    return points


def airports():
    # coordinates for each airport
    points = airports_as_points()
    plt.scatter(*zip(*points), edgecolors='blue', s=0.2)
    plt.show()


def edges_as_lines(graph):
    airport_dict = mk_airportdict()
    edges = graph.edges
    lines = []
    for pair in edges:
        lat1, lon1 = airport_dict[pair[0]]['lat'], airport_dict[pair[0]]['lon']
        lat2, lon2 = airport_dict[pair[1]]['lat'], airport_dict[pair[1]]['lon']
        point1 = (lon1, lat1)
        point2 = (lon2, lat2)
        lines.append([point1, point2])

    return lines


def plot_lines(lines, points, linewidth, pointsize):
    lc = LineCollection(lines, colors=['blue', 'gray', 'red', 'purple', 'green', 'orange',
                                       'cyan', 'pink'], linewidths=linewidth)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    # add lines to be plotted
    ax1.add_collection(lc)
    # store all x coordinates in points in a separate list
    x = [pair[0] for pair in points]
    # store all y coordinates in points in separate list
    y = [pair[1] for pair in points]
    # add these points
    ax1.scatter(x, y, s=pointsize)
    plt.show()


def routes():
    # get all lines to be plotted
    lines = edges_as_lines(mk_routegraph(mk_routeset()))
    # get all points to be plotted
    points = airports_as_points()
    # plot lines and points
    plot_lines(lines, points, 0.15, 0.15)


def k_spanning_tree(G=mk_routegraph(mk_routeset()), k=1000):
    # get minimum spanning tree
    MST = list(nx.algorithms.tree.mst.minimum_spanning_edges(G))
    # get weight for each edge
    weights = [MST[i][2]['weight'] for i in range(len(MST))]

    for j in range(k - 1):
        # get index of the the edge with max weight
        index_max = weights.index(max(weights))
        # remove that edge from the list
        del MST[index_max]
        # remove the weight from weights for updating index_max
        del weights[index_max]

    # new graph with the remaining edges
    new_G = nx.Graph(MST)
    # get the lines to be plotted
    lines = edges_as_lines(new_G)
    # get all points from root graph to be plotted, i.e all airports
    points = airports_as_points()
    # plot these lines and points
    plot_lines(lines, points, 1, 0.1)


def get_color(index):
    color = ['cyan', 'green', 'purple', 'red', 'blue', 'yellow',
                                       'gray', 'pink'] # or? list(matplotlib.colors.cnames.values())
    return color[index%len(color)]


def k_means(data=airports_as_points(), k=7):
    # customize data (airport points)
    arr = np.array(data)
    # get predict cluster index of each point
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=1).fit_predict(arr)
    for p in range(k):
        # get x coordinates for all points whose predict cluster index = p
        x = [arr[i][0] for i in range(len(arr)) if kmeans[i] == p]
        # get y coordinates for all points whose predict cluster index = p
        y = [arr[j][1] for j in range(len(arr)) if kmeans[j] == p]
        # store these points with in scatter in order to get the next set of points (whose predict cluster index=p+1)
        plt.scatter(x, y, s=0.1, c=get_color(p))

    plt.show()


def demo():
    if sys.argv[1] == 'airports':
        airports()
    elif sys.argv[1] == 'routes':
        routes()
    elif sys.argv[1] == 'span':
        if 2 < len(sys.argv):
            k_spanning_tree(k=int(sys.argv[2]))
        else:
            k_spanning_tree()
    elif sys.argv[1] == 'means':
        if 2 < len(sys.argv):
            k_means(k=int(sys.argv[2]))
        else:
            k_means()

if __name__ == '__main__':
    demo()



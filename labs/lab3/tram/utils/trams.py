import json
import os

from django.conf import settings

from .graphs import *
import sys

sys.path.append('../lab1/')
import tramdata as td

TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')


class TramStop:

    def __init__(self, name, lines=None, lat=None, lon=None):
        self.__name = name
        self.__position = ()
        self.__lines = []
        if lines is not None:
            self.__lines = lines
        if lat is not None and lon is not None:
            self.set_position(lat, lon)

    def get_name(self):
        return self.__name

    def get_position(self):
        return self.__position

    def get_lines(self):
        return self.__lines

    def set_position(self, lat, lon):
        self.__position = (lat, lon)

    def add_line(self, line):
        self._lines.append(line)


class TramLine:

    def __init__(self, name, stops):
        self.__name = name
        self.__stops = stops

    def get_name(self):
        return self.__name

    def get_stops(self):
        return self.__stops


class TramNetwork(WeightedGraph):

    def __init__(self, lines, stops, times, start=None):
        super(TramNetwork, self).__init__(start)
        self.__linedict = {}
        self.__stopdict = {}
        self._timedict = times
        # fill the __linedict with lines (key: line name, value: Tramline obj)
        for line in lines:
            line_obj = TramLine(line, lines[line])
            self.__linedict[line] = line_obj
            for i in range(len(lines[line]) - 1):
                a = lines[line][i]
                b = lines[line][i + 1]
                self.add_edge(a, b)
                time = td.time_between_stops(lines, times, line, a, b)
                self.set_weight(a, b, time)

        # fill the __stopdict with stops (key: stop name, value: Tramstop obj)
        for stop in stops:
            position = (float(stops[stop]['lat']), float(stops[stop]['lon']))
            stop_obj = TramStop(stop, td.lines_via_stop(lines, stop), position[0], position[1])
            self.__stopdict[stop] = stop_obj
            self.add_vertex(stop)
            self.set_vertex_value(stop, position)


    def all_lines(self):
        return [line for line in self.__linedict]

    def all_stops(self):
        return self.vertices()

    def line_stops(self, line):
        return self.__linedict[line].get_stops()

    def geo_distance(self, a, b):
        a_lat = float(self.__stopdict[a].get_position()[0])
        a_lon = float(self.__stopdict[a].get_position()[1])
        b_lat = float(self.__stopdict[b].get_position()[0])
        b_lon = float(self.__stopdict[b].get_position()[1])

        return (td.distance_between_two_points(a_lat, a_lon, b_lat, b_lon))

    def extreme_positions(self):
        res_dict = {'max_lat': 0, 'min_lat': float('inf'), 'max_lon': 0, 'min_lon': float('inf')}

        for stop in self.__stopdict:
            position = self.__stopdict[stop].get_position()
            # check if the current stop lat is larger than max_lat
            if position[0] > res_dict['max_lat']:
                res_dict['max_lat'] = position[0]
            # check if the current stop lat is smaller than min_lat
            elif position[0] < res_dict['min_lat']:
                res_dict['min_lat'] = position[0]
            # check if the current stop lon is larger than max_lon
            if position[1] > res_dict['max_lon']:
                res_dict['max_lon'] = position[1]
            # check if the current stop lat is smaller than min_lon
            elif position[1] < res_dict['min_lon']:
                res_dict['min_lon'] = position[1]

        return res_dict


    def stop_lines(self, stop):
        return self.__stopdict[stop].get_lines()

    def stop_position(self, stop):
        return self.__stopdict[stop].get_position()

    def transition_time(self, a, b):
        return self.get_weight(a, b)

class SpecTramNetwork(WeightedGraph):

    def __init__(self, tramnetwork, start=None):
        super(SpecTramNetwork, self).__init__(start)
        self._tmn = tramnetwork
        all_lines = tramnetwork.all_lines()
        all_stops = tramnetwork.all_stops()
        with open(TRAM_FILE, 'r', encoding='utf-8') as dict_file:
            data = json.load(dict_file)
        line_dict = data['lines']

        # loop to add an edge between all vertices whose stops are connected
        for line in all_lines:
            stops = tramnetwork.line_stops(line)
            for i in range(len(stops) - 1):
                a = (stops[i], line)
                b = (stops[i + 1], line)

                self.add_edge(a, b)
                time = td.time_between_stops(line_dict, tramnetwork._timedict, line, stops[i], stops[i + 1])
                self.set_weight(a, b, time)

        # loop to add an edge between all identical stops but that have different line
        for stop in all_stops:
            for l1 in tramnetwork.stop_lines(stop):
                for l2 in tramnetwork.stop_lines(stop):
                    if l1 != l2:
                        a = (stop, l1)
                        b = (stop, l2)
                        self.add_edge(a, b)
                        self.set_weight(a, b, 10)

        #for p1 in self.vertices():
        #    for i in range(self.vertices().index(p1), len(self.vertices())):
        #        c += 1
        #        p2 = self.vertices()[i]
        #        if p1[0] == p2[0]:
        #            self.add_edge(p1, p2)
        #            self.set_weight(p1, p2, 10)


def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile) as datafile:
        tramdict = json.load(datafile)

    stop_dict = tramdict['stops']
    line_dict = tramdict['lines']
    time_dict = tramdict['times']

    tnw = TramNetwork(line_dict, stop_dict, time_dict)
    return tnw


def specialize_stops_to_lines(network):
    return SpecTramNetwork(network)

def specialized_geo_distance(spec_network, a, b):
    stop1, stop2 = a[0], b[0]
    # 20 meters for the same stops
    if stop1 == stop2:
        return 0.02

    return spec_network._tmn.geo_distance(stop1, stop2)


def specialized_transition_time(spec_network, a, b):
    #stop1, stop2 = a[0], b[0]
    #print("stop1: " + stop1 + ", stop2: " + stop2)

    return spec_network.get_weight(a, b)

def get_path_cost(graph, path, geo_distance = False):
    cost = 0
    for i in range(len(path) - 1):
        if geo_distance:
            cost += specialized_geo_distance(graph, path[i], path[i+1])
        else:
            cost += specialized_transition_time(graph, path[i], path[i+1])

    return cost.__round__(3)



def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')
    view_shortest(G, a, b)
import time
start_time = time.time()
if __name__ == '__main__':
    pass

    #demo() (('Ullevi Södra', '13'), ('Centralstationen', '13'))
    #c = SpecTramNetwork(readTramNetwork())
    #print(len(c.edges()))
    #vertices: 352
    #edges: 340, 760
    #16.335265636444092
    #print("--- %s seconds ---" % (time.time() - start_time))

#dijkstra(readTramNetwork(),'Chalmers')
#print(dijkstra(SpecTramNetwork(readTramNetwork()), ('Centralstationen', '13')))
#print(('Chalmers', '6') in specialize_stops_to_lines(readTramNetwork()).neighbors(('Centralstationen', '7')))
#print(specialized_transition_time(specialize_stops_to_lines(readTramNetwork()), ('Centralstationen', '7'), ('Chalmers', '6')))
#print(specialized_geo_distance(specialize_stops_to_lines(readTramNetwork()), ('Centralstationen', '7'), ('Chalmers', '6')))
#print(specialized_geo_distance(specialize_stops_to_lines(readTramNetwork()), ('Chalmers', '7'), ('Chalmers', '6')))
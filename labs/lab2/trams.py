import json
from graphs import *
import sys

sys.path.append('../lab1/')
import tramdata as td

TRAM_FILE = '../lab1/tramnetwork.json'


class TramStop:

    def __init__(self, name, lines=None, lat=None, lon=None):
        self.__name = name
        self.__position = ()
        self.__lines = []
        if lines is not None:
            self._lines = lines
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
        self.__timedict = {}
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

        return td.distance_between_two_points(a_lat, a_lon, b_lat, b_lon)

    def extreme_position(self):
        res_dict = {'max_lat' : 0, 'min_lat' : float('inf'), 'max_lon' : 0, 'min_lon' : float('inf')}

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



def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile) as datafile:
        tramdict = json.load(datafile)

    stop_dict = tramdict['stops']
    line_dict = tramdict['lines']
    time_dict = tramdict['times']

    tnw = TramNetwork(line_dict, stop_dict, time_dict)
    return tnw

def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')
    view_shortest(G, a, b)

if __name__ == '__main__':
    pass
    #demo()

print(readTramNetwork().transition_time('Wavrinskys Plats', 'Chalmers'))
#print(readTramNetwork().stop_position('Chalmers'))
#print(readTramNetwork().get_vertex_value('Chalmers'))
#print(readTramNetwork().geo_distance('Chalmers', 'Järntorget'))
#print(readTramNetwork().extreme_position())
#print(dijkstra(readTramNetwork(), 'Chalmers')['Brunnsparken'])



import json
import sys
from graph import *
from tramdata import *


class TramStop:

    def __init__(self, name, lines=None, lat=None, lon=None):
        self.__name = name
        self.__position = ()
        self.__lines = []
        if lines is not None:
            self._lines = lines
        if lat is not None and lon is not None:
            self._position = (lat, lon)

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def get_lines(self):
        return self._lines

    def set_position(self, lat, lon):
        self._position = (lat, lon)

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

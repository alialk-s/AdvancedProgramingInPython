import unittest
import json
from labs.lab1 import tramdata
from labs.lab2 import trams

TRAM_FILE = '../lab1/tramnetwork.json'
tramnetwork_obj = trams.readTramNetwork()

class TestTrams(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            self.tramdict = json.loads(trams.read())
            self.stopdict = self.tramdict['stops']
            self.linedict = self.tramdict['lines']
            self.timesdict = self.tramdict['times']


    def test_all_lines(self):
        self.assertEqual(tramnetwork_obj.all_lines(), list(self.linedict.keys()))

    def test_all_stops(self):
        self.assertEqual(tramnetwork_obj.all_stops(), list(self.stopdict.keys()))

    def test_geo_distance(self):
        for a in tramnetwork_obj.all_stops():
            for b in tramnetwork_obj.all_stops():
                self.assertEqual(tramnetwork_obj.geo_distance(a, b), tramdata.distance_between_stops(self.stopdict, a, b))


    def test_extreme_positions(self):
        lats, lons = [], []

        for stop in self.stopdict:
            lats.append(self.stopdict[stop]['lat'])
            lons.append(self.stopdict[stop]['lon'])

        max_lat = max(lats)
        min_lat = min(lats)
        max_lon = max(lons)
        min_lon = min(lons)
        expected = {'max_lat': float(max_lat), 'min_lat': float(min_lat), 'max_lon': float(max_lon), 'min_lon': float(min_lon)}
        actual = tramnetwork_obj.extreme_position()

        self.assertEqual(str(expected), str(actual))

    def test_transition_time(self):
        for a in self.timesdict:
            for b in self.timesdict[a]:
                self.assertEqual(self.timesdict[a][b], tramnetwork_obj.transition_time(a, b))





if __name__ == '__main__':
    unittest.main()

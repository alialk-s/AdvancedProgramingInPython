import unittest
import json
from labs.lab2 import trams

TRAM_FILE = '../lab1/tramnetwork.json'
tramnetwork_obj = trams.readTramNetwork()

class MyTestCase(unittest.TestCase):

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

    def test_transition_time(self):
        for a in self.timesdict:
            for b in self.timesdict[a]:
                self.assertEqual(self.timesdict[a][b], tramnetwork_obj.transition_time(a, b))



if __name__ == '__main__':
    unittest.main()

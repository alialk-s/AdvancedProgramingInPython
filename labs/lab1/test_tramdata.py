import json
import unittest
from .tramdata import *


TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']


    # add your own tests here

    def test_times_between_stops(self):
        time = time_between_stops(self.linedict, self.timedict, 'Chalmers', 'Centralstationen')
        assert time == 8

if __name__ == '__main__':
    unittest.main()


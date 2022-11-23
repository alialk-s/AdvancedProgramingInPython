import json
import unittest
from tramdata import *

# TRAM_FILE = 'C:/Users/46707/Desktop/AdvancedPython/AdvancedProgramingInPython/labs/lab1/tramnetwork.json'
TRAM_FILE = 'tramnetwork.json'
# majority

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']
            self.tramdict = tramdict

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg=stop + ' not in stopdict')

    def test_lines_via_stop(self):
        actual = lines_via_stop(self.linedict, 'Chalmers')
        expected = ['6', '7', '8', '10', '13']
        self.assertEqual(expected, actual)

    def test_lines_via_stop_with_unknown_stop(self):
        actual = lines_via_stop(self.linedict, 'mystop')
        expected = []
        self.assertEqual(expected, actual)

    def test_lines_between_stops(self):
        actual = lines_between_stops(self.linedict, 'Vagnhallen Majorna', 'Brunnsparken')
        expected = ['3', '9']
        self.assertEqual(expected, actual)

    def test_lines_between_stops_no_lines_between(self):
        actual = lines_between_stops(self.linedict, 'Friskväderstorget', 'Nya Varvsallén')
        expected = []
        self.assertEqual(expected, actual)

    def test_time_between_stops(self):
        actual = time_between_stops(self.linedict, self.timedict, '7', 'Chalmers', 'Centralstationen')
        expected = 8
        self.assertEqual(expected, actual)

    def test_distance_between_stops(self):
        actual = distance_between_stops(self.stopdict, 'Chalmers', 'Järntorget')
        expected = 1.628
        self.assertEqual(expected, actual)

    def test_answer_query_via_stop(self):
        actual = answer_query(self.tramdict, 'via Hjalmar Brantingsplatsen')
        expected = ['5', '6', '10']
        self.assertEqual(expected, actual)

    def test_answer_query_between_stop1_and_stop2(self):
        actual = answer_query(self.tramdict, 'between Beväringsgatan and SKF')
        expected = ['6', '7', '11']
        self.assertEqual(expected, actual)

    def test_answer_query_time_with_line_from_stop1_to_stop2(self):
        actual = answer_query(self.tramdict, 'time with 4 from Centralstationen to Storås')
        expected = 11
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

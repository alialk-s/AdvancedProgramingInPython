import json
import unittest
from tramdata import *

TRAM_FILE = 'tramnetwork.json'


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']
            self.tramdict = tramdict

    def test_all_lines_exist_in_timedict(self):
        with open('tramlines.txt', 'r', encoding='utf-8') as txt_test:
            lines = txt_test.readlines()
        for i in range(len(lines)):
            if i == 0 or i - 1 > 0 and not lines[i - 1].strip():
                # update the line num to be current line
                line_num = lines[i].rstrip()
                # substring only the digit part
                line_num = line_num[0: len(line_num) - 1]
                # check this particular line in linedict
                self.assertIn(line_num, self.linedict)

    def test_all_stops_in_lines_exist_correctly_in_linedict(self):
        with open('tramlines.txt', 'r', encoding='utf-8') as txt_test:
            lines = txt_test.readlines()
            stops_list = []
        for i in range(len(lines)):
            if i == 0 or i - 1 > 0 and not lines[i - 1].strip():
                # update the line num to be current line
                line_num = lines[i].rstrip()
                # substring only the digit part
                line_num = line_num[0: len(line_num) - 1]
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        stop_name = get_stop_name(lines[j])
                        stops_list.append(stop_name)
                    else:
                        # test that the stops_list are equal to the corresponding list
                        self.assertEqual(self.linedict[line_num], stops_list)
                        stops_list = []
                        break

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg=stop + ' not in stopdict')

    # test for a helper function
    def test_get_stop_name(self):
        with open('tramlines.txt', 'r', encoding='utf-8') as test_txt_file:
            lines = test_txt_file.readlines()
        test_list = ['Östra Sjukhuset', 'Tingvallsvägen', 'Kaggeledstorget', 'Ättehögsgatan']
        for i in range(1, 5):
            stop_name = get_stop_name(lines[i])
            self.assertIn(stop_name, test_list)

    def test_time_between_two_stops_is_always_the_same(self):
        for a in self.stopdict:
            for b in self.stopdict:
                for line in lines_between_stops(self.linedict, a, b):
                    time_from_a_to_b = time_between_stops(self.linedict, self.timedict, line, a, b)
                    time_from_b_to_a = time_between_stops(self.linedict, self.timedict, line, b, a)

                    self.assertEqual(time_from_a_to_b, time_from_b_to_a)

    def test_all_distances_below_20(self):
        distance_limit = 20
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:
                distance = distance_between_stops(self.stopdict, stop1, stop2)
                self.assertTrue(distance < distance_limit)

    # test for a helper function
    def test_get_stop_time(self):
        with open('tramlines.txt', 'r', encoding='utf-8') as test_txt_file:
            lines = test_txt_file.readlines()
        test_list = ['10:35', '10:37', '10:38']
        for i in range(26, 30):
            stop_name = get_stop_time(lines[i])
            self.assertIn(stop_name, test_list)

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

    def test_answer_query_uninterpreted_input1(self):
        actual = answer_query(self.tramdict, 'VIa Chalmers')
        self.assertFalse(actual)

    def test_answer_query_uninterpreted_input2(self):
        actual = answer_query(self.tramdict, 'between Chalmers Centralstionen and')
        self.assertFalse(actual)

    def test_answer_query_uninterpreted_input3(self):
        actual = answer_query(self.tramdict, 'time 9 with from Brunnsparken to SKF')
        self.assertFalse(actual)

    def test_answer_query_uninterpreted_input4(self):
        actual = answer_query(self.tramdict, 'time with 9 from Brunnsparken SKF to')
        self.assertFalse(actual)

    def test_answer_query_uninterpreted_input5(self):
        actual = answer_query(self.tramdict, 'distance from Centralstationen toChalmers')
        self.assertFalse(actual)

    def test_answer_query_uninterpreted_input6(self):
        actual = answer_query(self.tramdict, 'please let me hack you')
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()

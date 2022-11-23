import json
import math
import sys


def build_tram_stops(jsonobject):
    with open(jsonobject, 'r') as dict_file:
        data = json.load(dict_file)

    stop_dict = {}  # a dict (of dicts) where the result will be stored
    for c in data:
        # store the positions in a smaller dict that will be the value of the returning dict
        short_dict = {'lat': data[c]['position'][0], 'lon': data[c]['position'][1]}
        # add positions of each stop as a dict into the returning dict
        stop_dict[c] = short_dict

    return stop_dict


def get_stop_name(line):
    # remove any white space from left and right
    stop_name = line.strip()
    # remove the time part
    stop_name = stop_name[:len(stop_name) - 5]
    # finally, remove the middle white space that existed between name and time
    stop_name = stop_name.rstrip()

    return stop_name


def get_stop_time(line):
    # remove any white space from left and right
    stop_time = line.strip()
    # substring the only time part
    stop_time = stop_time[len(stop_time) - 5: len(stop_time)]

    return stop_time


def calculate_stop_time_difference(time1, time2):
    return abs(int(time1[3: 5]) - int(time2[3: 5]))


def build_tram_lines(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    line_dict = {}  # the returning dict where all lines and their stops are stored
    stops_list = []  # the list of the stops of each line

    for i in range(len(lines)):
        # check that the line is not empty
        if lines[i].strip():
            # check the line where the line number exists
            if i == 0 or i - 1 > 0 and not lines[i - 1].strip():
                # update the key to be current line
                key = lines[i].rstrip()
                # substring only the digit part
                key = key[0: len(key) - 1]
            else:
                # add into the list stop(s) that belong to the current line (key)
                stops_list.append(get_stop_name(lines[i]))
        else:
            # store this line (key) with all its stops in the returning dict
            line_dict[key] = stops_list
            # update (clear) the list for storing the stops of next line
            stops_list = []

    return line_dict


def pairs_dict_connected_stops_time(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    dict_of_pairs = {}  # connected stops (as a pair) are keys and times between them are values
    for i in range(len(lines)):
        # check if the current line is representing an actual stop
        if len(lines[i].strip()) > 3:
            # check if the next line is representing an actual stop
            if i + 1 < len(lines) and len(lines[i + 1].strip()) > 3:
                # get stop name of the current line
                current_stop = get_stop_name(lines[i])
                # get stop name of the next line
                connected_stop = get_stop_name(lines[i + 1])
                # check if this pair is not already added to the dict
                if (current_stop, connected_stop) not in dict_of_pairs and (
                        connected_stop, current_stop) not in dict_of_pairs:
                    # get stop time of the current line
                    current_stop_time = get_stop_time(lines[i])
                    # get stop time of the next line
                    connected_stop_time = get_stop_time(lines[i + 1])
                    # calculate difference between them
                    time_difference = calculate_stop_time_difference(current_stop_time, connected_stop_time)
                    # finally, add the pair into the dict
                    dict_of_pairs[(current_stop, connected_stop)] = time_difference
            # check if the previous line is representing an actual stop
            if i - 1 >= 0 and len(lines[i - 1].strip()) > 3:
                # get stop name of the current line
                current_stop = get_stop_name(lines[i])
                # get stop name of the previous line
                connected_stop = get_stop_name(lines[i - 1])
                # check if this pair is not already added to the dict
                if (current_stop, connected_stop) not in dict_of_pairs and (
                        connected_stop, current_stop) not in dict_of_pairs:
                    # get stop time of the current line
                    current_stop_time = get_stop_time(lines[i])
                    # get stop time of the previous line
                    connected_stop_time = get_stop_time(lines[i - 1])
                    # calculate difference between them
                    time_difference = calculate_stop_time_difference(current_stop_time, connected_stop_time)
                    # finally, add the pair into the dict
                    dict_of_pairs[(current_stop, connected_stop)] = time_difference

    return dict_of_pairs


def build_tram_times(txt_file):
    dict_pairs = pairs_dict_connected_stops_time(txt_file)  # check what dict_connected_stops_times() returns for smother
    # understanding
    time_dict = {}  # the returning the dict, dict of dicts
    for pair in dict_pairs:
        # if first stop in the pair doesn't exist as a key
        if pair[0] not in time_dict:
            # if the second stop in the pair doesn't exist as well
            if pair[1] not in time_dict:
                # make the first stop in the pair to be the key of the returning dict
                out_key = pair[0]
                # make the second stop in the pair to be the key of the inner dict
                inner_key = pair[1]
                # create a new (inner) dict
                value = {inner_key: dict_pairs[pair]}
                # add this created dict to the returning dict
                time_dict[out_key] = value
            # if the second stop exists as a key
            else:
                # the key of the inner dict
                inner_key = pair[0]
                # the key of the returning dict
                out_key = pair[1]
                # the value is the distance between these two stops in the pair
                value = dict_pairs[pair]
                # finally, add it to dict (under the second stop in the pair, pair[1])
                time_dict[out_key][inner_key] = value
        else:
            # the key of the inner dict
            inner_key = pair[1]
            # the key of the returning dict
            out_key = pair[0]
            # the value is the distance between these two stops in the pair
            value = dict_pairs[pair]
            # finally, add it to dict (under the first stop in the pair, pair[0])
            time_dict[out_key][inner_key] = value

    return time_dict


def build_tram_network(json_file, txt_file):
    # dict of stops
    dict1 = build_tram_stops(json_file)
    # dict of lines
    dict2 = build_tram_lines(txt_file)
    # dict of times
    dict3 = build_tram_times(txt_file)
    # combine all the previous dicts to result dict
    res_dict = {'stops': dict1, 'lines': dict2, 'times': dict3}
    # open json file, or create it if not exists
    out_file = open("tramnetwork.json", "w")
    # convert the result dict to json
    json.dump(res_dict, out_file, indent=6)
    # close file
    out_file.close()

    return out_file


def lines_via_stop(lines_dict, stop):
    return [k for k in lines_dict if stop in lines_dict[k]]


def lines_between_stops(line_dict, stop1, stop2):
    return [k for k in line_dict if stop1 in line_dict[k] and stop2 in line_dict[k]]


def time_between_stops(lines_dict, times_dict, line, stop1, stop2):
    line_str = str(line)
    if line_str in lines_between_stops(lines_dict, stop1, stop2):
        # get all stops in this line
        all_stops_in_line = [s for s in lines_dict[line_str]]
        # get the min index of stop1 and stop2 in the list
        min_index = min(all_stops_in_line.index(stop1), all_stops_in_line.index(stop2))
        # get the max index of stop1 and stop2 in the list
        max_index = max(all_stops_in_line.index(stop1), all_stops_in_line.index(stop2))
        # get all stops between stop1 and stop, including stop1 and stop2
        stops_in_between = [all_stops_in_line[i] for i in range(min_index, max_index + 1)]
        # time between stop
        total_time = 0
        # loop over all stops between stop1 and stop2
        for i in range(len(stops_in_between) - 1):
            # first stop of the connected stop
            st1 = stops_in_between[i]
            # second stop of the connected stop
            st2 = stops_in_between[i + 1]
            # get time between them if st1 is the key in the time dict
            if st1 in times_dict.keys() and st2 in times_dict[st1].keys():
                # add time between these two stops into the total time
                total_time += times_dict[st1][st2]
            # get time between them if st2 is the key in the time dict
            elif st2 in times_dict.keys() and st1 in times_dict[st2].keys():
                # add time between these two stops into the total time
                total_time += times_dict[st2][st1]
        return total_time
    else:
        raise Exception("No such pair of stops in this line")


def distance_between_stops(stop_dict, stop1, stop2):
    if stop1 not in stop_dict or stop2 not in stop_dict:
        return -1
    else:
        # get stop1 position information from stop dict
        stop1_position = [stop_dict[c] for c in stop_dict if c == stop1][0]
        # get stop2 position information from stop dict
        stop2_position = [stop_dict[c] for c in stop_dict if c == stop2][0]
        # stop1 latitude
        stop1_lat = float(stop1_position['lat'])
        # stop1 longitude
        stop1_lon = float(stop1_position['lon'])
        # stop2 latitude
        stop2_lat = float(stop2_position['lat'])
        # stop2 longitude
        stop2_lon = float(stop2_position['lon'])
        # radius of the earth in km
        R = 6371.009
        # mean latitude
        mean_lat = ((stop1_lat + stop2_lat) * (math.pi / 180)) / 2
        # delta latitude
        delta_lat = (stop1_lat - stop2_lat) * (math.pi / 180)
        # delta longitude
        delta_lon = (stop1_lon - stop2_lon) * (math.pi / 180)
        # calculate distance using the formula for Spherical Earth projected to a plane
        distance = R * math.sqrt(math.pow(delta_lat, 2) + math.pow(math.cos(mean_lat) * delta_lon, 2))

        return distance.__round__(3)


def answer_query(tramdict, query):
    # remove any double white space from right, left or in between
    user_input = " ".join(query.split())
    # convert the string to a list for easier indexing and slicing
    user_input_as_list = user_input.split(' ')
    # if the query is via <stop>
    if user_input[:3] == 'via':
        stop1 = user_input[4: len(user_input)]
        # get list of all possible traffic lines
        ans = lines_via_stop(tramdict['lines'], stop1)
        if len(ans) == 0:
            ans = -1
    # if the query is between <stop1> and <stop2>
    elif user_input[:8] == 'between ' and 'and' in user_input_as_list:
        # get stop1 name by slicing user_input_as_list and then converting it to a string again
        stop1 = ' '.join(
            user_input_as_list[user_input_as_list.index('between') + 1: user_input_as_list.index('and')])
        # get stop2 name by slicing user_input_as_list and then converting it to a string again
        stop2 = ' '.join(user_input_as_list[user_input_as_list.index('and') + 1: len(user_input_as_list)])
        # get possible lines through these two stops
        ans = lines_between_stops(tramdict['lines'], stop1, stop2)
        # check if no such stops
        if stop1 not in tramdict['stops'] or stop2 not in tramdict['stops']:
            ans = -1

    # check if the query is time with <line> from <stop1> to <stop2>
    elif user_input[
         :10] == 'time with ' and 'from' in user_input_as_list and 'to' in user_input_as_list and user_input_as_list.index(
        'with') + 1 < user_input_as_list.index('from') < user_input_as_list.index('to') - 1 < len(
        user_input_as_list) - 2:
        # get line name by slicing user_input_as_list from 'with' to 'from', and then reconverting it to a string
        line = ' '.join(user_input_as_list[user_input_as_list.index('with') + 1: user_input_as_list.index('from')])
        # get stop1 name by slicing user_input_as_list from 'from' to 'to', and then reconverting it to a string
        stop1 = ' '.join(user_input_as_list[user_input_as_list.index('from') + 1: user_input_as_list.index('to')])
        # get stop2 name by slicing user_input_as_list from 'to' to last element, and then reconverting it to a string
        stop2 = ' '.join(user_input_as_list[user_input_as_list.index('to') + 1: len(user_input_as_list)])
        if line not in tramdict['lines'] or stop1 not in tramdict['stops'] or stop2 not in tramdict['stops']:
            ans = -1
        else:
            ans = time_between_stops(tramdict['lines'], tramdict['times'], line, stop1, stop2)

    # check if the query is distance from <stop1> to <stop2>
    elif user_input[:14] == 'distance from ' and 'to' in user_input_as_list and user_input_as_list.index(
            'from') + 1 < user_input_as_list.index(
        'to') < len(user_input_as_list) - 1:
        # get stop1 name by slicing user_input_as_list from 'from' to 'to', and then converting it to a string again
        stop1 = ' '.join(user_input_as_list[user_input_as_list.index('from') + 1: user_input_as_list.index('to')])
        # get stop2 name by slicing user_input_as_list from 'to' to last element, and then reconverting it to a string
        stop2 = ' '.join(user_input_as_list[user_input_as_list.index('to') + 1: len(user_input_as_list)])
        # get distance between stop1 and stop2
        ans = distance_between_stops(tramdict['stops'], stop1, stop2)
    else:
        ans = False

    return ans


def dialogue(jsonfile):
    with open(jsonfile) as final_file:
        tramdict = json.load(final_file)
    # this decide whenever the loop must be terminated
    get_more_input = True
    while get_more_input:
        # get user input
        user_input = input()
        # if quit
        if user_input == 'quit':
            # terminate the loop
            get_more_input = False
        else:
            try:
                # send query for processing and getting an answer back
                ans = answer_query(tramdict, user_input)
                # answer_query return -1 in those cases when arguments are invalid
                if ans == -1:
                    ans = 'unknown arguments'
                # if the answer is False
                elif type(ans) is not list and not ans:
                    ans = 'sorry, try again'
                # exception could occur from the function time_between_stops()
            except Exception as e:
                ans = str(e)
            print(ans)


if __name__ == '__main__':
        if sys.argv[1:] == ['init']:
            build_tram_network()
        else:
            dialogue('tramnetwork.json')
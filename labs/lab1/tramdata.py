import json


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
    line_list = line.split(' ')
    stop_name = line_list[0]
    i = 1
    # add all words if the name isn't a single word
    while line_list[i]:
        stop_name += " " + line_list[i]
        i += 1
    return stop_name


def build_tram_lines(txt_file):
    with open(txt_file, 'r') as file:
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
            else:
                # add into the list stop(s) that belong to the current line (key)
                stops_list.append(get_stop_name(lines[i]))
        else:
            # store this line (key) with all its stops in the returning dict
            line_dict[key] = stops_list
            # update (clear) the list for storing the stops of next line
            stops_list = []

    return line_dict



if __name__ == '__main__':
    print(build_tram_stops('tramstops.json'))
    print((build_tram_lines('tramlines.txt')))
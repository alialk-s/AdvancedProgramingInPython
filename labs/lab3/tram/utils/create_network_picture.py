# baseline tram visualization for Lab 3
# creates by default an SVG image usable on the home page
# this image can then be coloured by using tramviz.py, which operates directly on the SVG file
# you don't need to use this file unless you want to use your own gbg_tramnet.svg
# this will be needed in Bonus task 2, where you change the URLs of vertices
# but you should only do this once, not every time you display a route
# rename the resulting file to gbg_tramnet.svg when you have your final version

from trams import readTramNetwork
import graphviz
import json
import os
from bs4 import BeautifulSoup
import requests
import re


MY_GBG_SVG = 'gbg_tramnet.svg'  # the output SVG file
MY_TRAMNETWORK_JSON = 'tramnetwork.json'  # JSON file from lab1
TRAM_URL_FILE = '../../static/tram_stops_urls.json'  # given in lab3/files, replace with your own in bonus 2
VASTTRAFIK_URL = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'
ANSLAG_TAVLA = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid='
DOC = BeautifulSoup(requests.get(VASTTRAFIK_URL).text, 'html.parser')


# assign colors to lines, indexed by line number; not quite accurate
gbg_linecolors = {
    1: 'gray', 2: 'yellow', 3: 'blue', 4: 'green', 5: 'red',
    6: 'orange', 7: 'brown', 8: 'purple', 9: 'cyan',
    10: 'lightgreen', 11: 'black', 13: 'pink'}


# compute the scale of the map; you may want to test different heuristics to make map look better
def scaled_position(network):
    positions = network.extreme_positions()
    minlat, minlon, maxlat, maxlon = positions['min_lat'], positions['min_lon'], positions['max_lat'], positions['max_lon']
    size_x = maxlon - minlon
    scalefactor = len(network) / 4  # heuristic
    x_factor = scalefactor / size_x
    size_y = maxlat - minlat
    y_factor = scalefactor / size_y

    return lambda xy: (x_factor * (xy[0] - minlon), y_factor * (xy[1] - minlat))


# Bonus task 2: create a json file that returns the actual traffic information, and rerun the map creation
def get_stop_gid(stop):
    # get html part associated with this stop
    stop_html = DOC.find(text=re.compile(stop)).parent
    # get the href out of it
    stop_href = stop_html['href']
    # finally, substring href to get the gid
    gid = stop_href.split('/')[3]

    return gid


def mk_gid_url_json():
    # stop name: url
    url_dict = {}
    # loop over all tram stops to build their gid
    for stop in readTramNetwork().all_stops():
        # get gid for this stop
        gid = get_stop_gid(stop)
        # store gid with associated stop name in url dict
        url_dict[stop] = ANSLAG_TAVLA+gid

    out_file = open(TRAM_URL_FILE, "w")
    # convert the result dict to json
    json.dump(url_dict, out_file, indent=6)
    # close file
    out_file.close()

    return out_file

def run_json(json_file):
    if not os.path.exists(json_file):
        mk_gid_url_json()

def stop_url(stop):
    with open(TRAM_URL_FILE) as file:
        stop_urls = json.loads(file.read())
    return stop_urls.get(stop, '.')


# You don't probably need to change this, if your TramNetwork class uses the same
# method names and types and represents positions as ordered pairs.
# If not, you will need to change the method call to correspond to your class.

def network_graphviz(network, outfile=MY_GBG_SVG, positions=scaled_position):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})

    for stop in network.all_stops():

        x, y = network.stop_position(stop)
        if positions:
            x, y = positions(network)((x, y))
        pos_x, pos_y = str(x), str(y)

        col = 'white'

        dot.node(stop, label=stop, shape='rectangle', pos=pos_x + ',' + pos_y + '!',
                 fontsize='8pt', width='0.4', height='0.05',
                 URL=stop_url(stop),
                 fillcolor=col, style='filled')

    for line in network.all_lines():
        stops = network.line_stops(line)
        for i in range(len(stops) - 1):
            dot.edge(stops[i], stops[i + 1],
                     color=gbg_linecolors[int(line)], penwidth=str(2))

    dot.format = 'svg'
    s = dot.pipe().decode('utf-8')
    with open(outfile, 'w') as file:
        file.write(s)


if __name__ == '__main__':
    run_json(TRAM_URL_FILE)
    network = readTramNetwork(tramfile=MY_TRAMNETWORK_JSON)
    network_graphviz(network)
    #print(stop_url('Chalmers'))

"""
# this is how the url json file was created
    import urllib.parse
    dict = {}
    google_url = 'https://www.google.com/search'
    for stop in network.all_stops():
        attrs = urllib.parse.urlencode({'q': 'Gothenburg ' + stop})
        dict[stop] = google_url + '?' + attrs
    with open(TRAM_URL_FILE, 'w') as file:
        json.dump(dict, file, indent=2, ensure_ascii=False)
"""
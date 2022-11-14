# Question 1

import csv  # https://docs.python.org/3/library/csv.html


def convert_value(s):
    try:
        converted = int(s)
    except ValueError:
        converted = s
    return converted


def tsv2list(file):
    with open(file, 'r', encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter='\t')
        data = [row for row in rows]
    list_dict = []
    for i in range(1, len(data)):
        dict_keys = {}
        for j in range(len(data[0])):
            key = data[0][j]
            dict_keys[key] = convert_value(data[i][j])

        list_dict.append(dict_keys)

    return list_dict


# Question 2

def tsv2dict(file, key=None):
    dict_list = tsv2list(file)
    if key is None:
        return dict_list
    else:
        if key not in dict_list[0].keys():
            print('None valid key')
            return None
        else:
            if key in ['country', 'capital']:
                res_dict = {}
                for dict_element in dict_list:
                    short_dict = dict_element.copy()
                    del short_dict[key]
                    res_dict[dict_element[key]] = short_dict
            else:
                print('None unique key')
                return None

    return res_dict


# Question 3

import json  # https://docs.python.org/3/library/json.html


def data2json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f)


def json2data(file):
    with open(file) as f:
        return json.load(f)


def test_json_data(file, key=None):
    obj = tsv2dict(file, key)
    json_path = "countries.json"
    data2json(obj, json_path)
    return json2data(json_path) == obj


# Question 4

def data2txt(data):
    pass


# Question 5

def n_countries(data):
    return len(data)


def most_common_currency(data):
    list_currency = [c for c in data if data[c].keys() == 'currency']

    return list_currency


def least_population_difference(data):
    pass


def countries_by_density(data):
    pass


def query_test():
    d = tsv2dict('countries.tsv', key='country')
    print("How many countries are there?")
    print(n_countries(d))
    print("What is the most common name of a currency?")
    print(most_common_currency(d))
    print("Which two countries have the smallest difference in population?")
    print(least_population_difference(d))
    print("List the 20 countries with the highest population density"
          + " population divided by area), together with the densities, in a "
          + "descending order of density.")
    print(countries_by_density(d)[:20])


##print(tsv2list('countries.tsv'))
#print(tsv2dict('countries.tsv', 'country'))

print(test_json_data('countries.tsv', 'country'))
#query_test()

print(most_common_currency(tsv2dict('countries.tsv', key='country')))





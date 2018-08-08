from optimus.helpers.constants import *

import json
import math

confidence_level_constant = [50, .67], [68, .99], [90, 1.64], [95, 1.96], [99, 2.57]


def fill_missing_col_types(col_types):
    """
    Fill missing col types with 0
    :param col_types:
    :return:
    """
    for label in PROFILER_COLUMN_TYPES:
        if label not in col_types:
            col_types[label] = 0
    return col_types


def fill_missing_var_types(var_types):
    """
    Fill missing data types with 0
    :param var_types:
    :return:
    """
    for label in PROFILER_TYPES:
        if label not in var_types:
            var_types[label] = 0
    return var_types


# TODO: Maybe use pprint instead of this
def print_json(value):
    """
    Print beauty jsons
    :return:
    """
    print(json.dumps(value, indent=2))


def write_json(data, path):
    """
    Write a json file with the profiler result
    :param data:
    :param path:
    :return:
    """

    with open(path, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def human_readable_bytes(num, suffix='B'):
    """
    Return a human readable file size
    :param num:
    :param suffix:
    :return:
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def sample_size(population_size, confidence_level, confidence_interval):
    """
    Get a sample number of the whole population
    :param population_size:
    :param confidence_level:
    :param confidence_interval:
    :return:
    """
    z = 0.0
    p = 0.5
    e = confidence_interval / 100.0
    n = population_size

    # Loop through supported confidence levels and find the num sdd deviations for that confidence level
    for i in confidence_level_constant:
        if i[0] == confidence_level:
            z = i[1]

    if z == 0.0:
        return -1

    # Calculate sample size
    n_0 = ((z ** 2) * p * (1 - p)) / (e ** 2)

    # Adjust sample size fo finite population
    n = n_0 / (1 + ((n_0 - 1) / float(n)))

    return int(math.ceil(n))  # THE SAMPLE SIZE
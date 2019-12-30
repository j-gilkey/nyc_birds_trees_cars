from ebird.api import get_observations
from ebird.api import get_regions, get_adjacent_regions, get_region
import config
import pandas as pd
import numpy as np
import mysql_functions as my_f

def get_nyc_obsv():
    api_key = config.ebird_api_key
    nyc_counties = ['US-NY-005', 'US-NY-047', 'US-NY-081', 'US-NY-061', 'US-NY-085']
    records = get_observations(api_key, nyc_counties, back=30)
    return records


def bird_parser(records):
    for bird in records:
        try:
            bird_tuple = (bird['speciesCode'], bird['comName'], bird['sciName'], bird['locId'], bird['locName'], bird['obsDt'], bird['howMany'], bird['lat'], bird['lng'])
            my_f.insert_bird(bird_tuple)
        except:
            print('Missing an attribute')
    return


#bird_parser(get_nyc_obsv())

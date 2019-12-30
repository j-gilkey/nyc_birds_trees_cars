from ebird.api import get_observations
from ebird.api import get_regions, get_adjacent_regions, get_region
import config
import pandas as pd
import numpy as np

api_key = config.ebird_api_key

nyc_counties = ['US-NY-005', 'US-NY-047', 'US-NY-081', 'US-NY-061', 'US-NY-085']

records = get_observations(api_key, nyc_counties, back=30)

print(len(records))


for bird in records:
    print(bird)

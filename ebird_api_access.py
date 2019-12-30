import requests
import time
import config
import mysql_functions

api_key = config.ebird_api_key

def bird_paginate():
    url = 'https://api.ebird.org/v2/data/obs/' + 'US-NY-005' +  '/historic/' + '2019' + '/' + '01' + '/' + '01'

    url_params = {
                    'api_key' : api_key
                }
    response = requests.get(url, params=url_params)
    print(response)
    data = response.json()


bird_paginate()

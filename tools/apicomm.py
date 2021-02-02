from movements import app

import requests

def getApiData(url, *params):
    url = url.format(*params)
    results = requests.get(url)

    if results.status_code == 200:
        return results.json()
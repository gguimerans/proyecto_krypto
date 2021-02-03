from movements import app

import requests

class PeticionError(Exception):
    pass

class CryptoAPI:
    def __init__(self, url, key):
        self.url = url
        self.key = key

    def consultaApi(self, params):
        
        url = self.url.format(params[0], params[1], params[2], self.key)
        results = requests.get(url)
        if results.status_code == 200:
            datos = results.json()
            if datos["status"]["error_code"] != 0:
                raise PeticionError(datos["status"]["error_message"])
            else:
                return datos
        else:
            raise PeticionError("Error en consulta: {}".format(results.status_code))
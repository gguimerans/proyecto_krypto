## Instalación

La instalación de esta aplicación se realiza sobre python3


## Instalación de dependencias:

1. Instalar python3 introduciendo el siguiente código en el terminal:
```$ sudo apt-get update```
```$ sudo apt-get install python3.6```


2. Instalar SQLITE3
   
```$ sudo apt update```
```$ sudo apt install sqlite3```

3. Crear y activar un entorno virtual para poder ejecutar la aplicación:

   - Crear el entorno 
```python -m venv venv```

    - Activar el entorno virtual
  
        Windows: venv\Scripts\activate
        Mac y Linux: . venv/bin/activate

    - Crear las variables del entorno

    ```pip install python - dotenv```

    - Crear archivo .env:

        FLASK_APP=run.py
        FLASK_ENV=development

## Obtener API key de coinmarketcap:

    Acceder a la URL:https://coinmarketcap.com/api/ y registrarse de modo gratuito para obtener su API Key

## Fichero de configuración:

    Renombre su config_template.py como config.py.
    Introducir una clave secreta.
    Introducir la API KEY obtenida.
    Introducir la ruta a la base de datos.

## Ejecución:

    En el terminal, volver a la carpeta raíz y ejecutar python run.py

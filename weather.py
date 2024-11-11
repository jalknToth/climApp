import dotenv as dt
import pprint as pp
import requests as rq
import os

# Cargando las variables de entorno desde el archivo .env
dt.load_dotenv()
# Función para obtener el clima de una ciudad específica.
# Recibe la ciudad, unidades y lenguaje como parámetros.
def revisarClima(city="Medellin", units="metric", lang="es"):
    
    try:
        # Construir la URL de la solicitud a la API de OpenWeatherMap
        request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units={units}&lang={lang}'
        # Solicitando GET a la API
        response = rq.get(request_url)
        # Verificando si la solicitud fue exitosa, si no, lanza una excepción
        response.raise_for_status()  
        # Convirtiendo la respuesta a formato JSON
        weather_data = response.json()
        # Devolviendo los datos del clima
        return weather_data
    except rq.exceptions.RequestException as e:
        # Manejando las excepciones en caso de error en la solicitud
        print(f"Error al obtener el clima: {e}")
        # Devolviendo None en caso de error
        return None

if __name__ == "__main__":
    # Imprimiendo el título del programa
    print('\n*** Revisar el clima ***\n')

    # Solicitando la ciudad
    city = input("\nBusca por ciudad: ")

    # Llamar a la función revisarClima para obtener los datos del clima
    weather_data = revisarClima(city)

    # Si se obtuvieron datos del clima, imprimirlos en pantalla
    if weather_data:
        print("\n")
        pp.pprint(weather_data)
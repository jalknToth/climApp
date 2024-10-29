import dotenv as dt
import pprint as pp
import requests as rq
import os

dt.load_dotenv()

def revisarClima(city="Medellin", units="metric", lang="es"):
    try:
        request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units={units}&lang={lang}'
        response = rq.get(request_url)
        response.raise_for_status()  
        weather_data = response.json()
        return weather_data
    except rq.exceptions.RequestException as e:
        print(f"Error al obtener el clima: {e}")
        return None

if __name__ == "__main__":
    print('\n*** Revisar el clima ***\n')

    city = input("\nBusca por ciudad: ")

    weather_data = revisarClima(city)

    if weather_data:
        print("\n")
        pp.pprint(weather_data)
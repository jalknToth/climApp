import flask as fk
import weather as wr
import waitress as wss

app = fk.Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return fk.render_template('index.html')

@app.route('/weather')
def get_weather():
    city = fk.request.args.get('city')

    if city is None or not city.strip():
        city = "Medellin"

    weather_data = wr.revisarClima(city)

    if weather_data is None:
        return fk.render_template('error.html', error_message="Error al obtener los datos del clima."), 500

    if weather_data['cod'] != 200:
        return fk.render_template('error.html', ciudad=city), 404

    return fk.render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == "__main__":
    wss.serve(app, host="0.0.0.0", port=8000)
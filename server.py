import flask as fk
import weather as wr
import waitress as wss
import mysql.connector as sql
import datetime as dt

app = fk.Flask(__name__)

def getDBconnection():
    conn = sql.connect(
        host='localhost',
        user='root',
        password='mefort@1ece',
        database='climapp'
    )
    return conn

def guardarDatos(ciudad,temperatura,descripcion):
    conn = getDBconnection()
    cur = conn.cursor()
    now = dt.datetime.now()
    try:
        cur.execute('INSERT INTO clima (ciudad, temperatura, descripcion, fecHora) VALUES (%s, %s, %s, %s)',(ciudad, temperatura, descripcion, now))
        conn.commit()
    except sql.Error as err:
        print(f"Error al guardar los datos: {err}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

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
    
    guardarDatos(weather_data["name"], weather_data['main']['temp'],weather_data["weather"][0]["description"])

    return fk.render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )
    
def creaTable():
    conn = getDBconnection()
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS clima (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ciudad VARCHAR(255) NOT NULL,
                        temperatura FLOAT,
                        descripcion VARCHAR(255),
                        fecHora DATETIME
                    )''')
        conn.commit()
    except sql.Error as err:
        print(f"Error al crear la tabla: {err}")
    finally:
        cur.close()
        conn.close()
        
if __name__ == "__main__":
    creaTable()
    wss.serve(app, host="0.0.0.0", port=8000)
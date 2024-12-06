# Importa las bibliotecas necesarias
import flask as fk  # Framework web Flask
import weather as wr  # Módulo personalizado para obtener datos del clima
import waitress as wss  # Servidor WSGI de producción para Flask
import mysql.connector as sql  # Conector para MySQL
import datetime as dt  #fechas y horas


# Creando una instancia de la aplicación Flask
app = fk.Flask(__name__)

# Conectando a la base de datos MySQL
def getDBconnection():
    conn = sql.connect(
        host='localhost',  # Host de la base de datos
        user='root',  # Usuario de la base de datos
        password='',  # Contraseña del usuario
        database='climapp'  # Nombre de la base de datos
    )
    return conn

# Guardando los datos del clima en la base de datos
def guardarDatos(ciudad, temperatura, descripcion):
    conn = getDBconnection()  # Obteniendo la conexión a la base de datos
    cur = conn.cursor()  # Cursor para ejecutar consultas
    now = dt.datetime.now()  # Obteniendo la fecha y hora actual

    try:
        # Insertando los datos en la tabla 'clima'
        cur.execute('INSERT INTO clima (ciudad, temperatura, descripcion, fecHora) VALUES (%s, %s, %s, %s)',(ciudad, temperatura, descripcion, now))
        conn.commit()  # Confirmando los cambios
    except sql.Error as err:  # Manejando errores de SQL
        print(f"Error al guardar los datos: {err}")
        conn.rollback()  # Revirtiendo los cambios en caso de error
    finally:
        cur.close()  # Cerrando el cursor
        conn.close()  # Cerrando la conexión


# Definiendo la ruta principal de la aplicación
@app.route('/')
@app.route('/index') # también respondiendo a /index
def index():
    return fk.render_template('index.html')  # Renderizando la plantilla 'index.html'


# Definiendo la ruta para obtener el clima
@app.route('/weather')
def get_weather():
    city = fk.request.args.get('city')  # Obteniendo el parámetro 'city'

    # Por defecto a "Medellin"
    if city is None or not city.strip():
        city = "Medellin"

    # Llama a la función 'revisarClima' del módulo 'weather' para obtener los datos del clima
    weather_data = wr.revisarClima(city)

    # Manejo de errores:
    if weather_data is None:
        return fk.render_template('error.html', error_message="Error al obtener los datos del clima."), 500  # Error 500: Internal Server Error

    if weather_data['cod'] != 200: # Si la API del clima devuelve un código distinto a 200 (OK)
        return fk.render_template('error.html', ciudad=city), 404  # Error 404: Not Found

    # Guardando los datos del clima en la base de datos
    guardarDatos(weather_data["name"], weather_data['main']['temp'], weather_data["weather"][0]["description"])

    # Renderizando la plantilla 'weather.html' con los datos del clima
    return fk.render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}", # Formatea la temperatura a un decimal
        feels_like=f"{weather_data['main']['feels_like']:.1f}" # Formatea la sensación térmica a un decimal
    )

# Función para crear la tabla 'clima' en la base de datos si no existe
def creaTable():
    conn = getDBconnection()
    cur = conn.cursor()

    try:
        # Crea la tabla 'clima'
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

# Punto de entrada principal del script
if __name__ == "__main__":
    creaTable()  # Creando la tabla al iniciar la aplicación
    wss.serve(app, host="0.0.0.0", port=8000)  # Iniciando el servidor Waitress en el puerto 8000 (para producción)